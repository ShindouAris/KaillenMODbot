import disnake
from disnake.ext import commands
from utils.ClientUser import ClientUser
from utils.error import ArgumentParsingError, GenericError
from zipfile import ZipFile
import os
import shutil
from typing import Union, Optional
import asyncio
import argparse

def format_git_log(data_list: list):

    data = []

    for d in data_list:
        if not d:
            continue
        t = d.split("*****")
        data.append({"commit": t[0], "abbreviated_commit": t[1], "subject": t[2], "timestamp": t[3]})

    return data

class CommandArgparse(argparse.ArgumentParser):

    def __init__(self, *args, **kwargs):

        kwargs.pop('exit_on_error', None)
        kwargs.pop('allow_abbrev', None)
        kwargs.pop('add_help', None)

        try:
            super().__init__(*args, exit_on_error=False, allow_abbrev=False, add_help=False, **kwargs)
        except TypeError:
            super().__init__(*args, allow_abbrev=False, add_help=False, **kwargs)

    def parse_known_args(
        self, args = None, namespace = None
    ):
        try:
            return super().parse_known_args(args, namespace)
        except argparse.ArgumentError as e:
            if "ignored explicit argument" not in str(e):
                raise e

            for arg_name in e.argument_name.split("/"):
                for c, a in enumerate(args):
                    if a.startswith(arg_name):
                        args[c] = a.replace("-", "", count=1)
                        return self.parse_known_args(args, namespace)

    def error(self, message: str):
        raise ArgumentParsingError(message)

class ShellResult:

    def __init__(self, status: int, stdout: Optional[bytes], stderr: Optional[bytes]):
        self.status = status
        self.stdout = stdout.decode(encoding="utf-8", errors="replace") if stdout is not None else None
        self.stderr = stderr.decode(encoding="utf-8", errors="replace") if stderr is not None else None


async def run_command(cmd: str):

    p = await asyncio.create_subprocess_shell(
        cmd, stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )
    stdout, stderr = await p.communicate()
    r = ShellResult(p.returncode, stdout, stderr)
    if r.status != 0:
        raise GenericError(f"{r.stderr or r.stdout}\n\nStatus Code: {r.status}")
    return str(r.stdout)

class Owner(commands.Cog):
    def __init__(self, bot: ClientUser):
        self.bot = bot
        
    async def reload_module(self):
    
        self.bot.load_modules()
        self.bot.load_events()
            
        
        
    @commands.is_owner()
    @commands.slash_command(name="reload", description="Tải lại các module")
    async def _reload_module(self, ctx: disnake.ApplicationCommandInteraction):
        await ctx.response.defer()
        await self.reload_module()
        await ctx.edit_original_response("Đã tải lại các module và event")
        
    update_flags = CommandArgparse()
    update_flags.add_argument("-force", "--force", action="store_true",
                              help="Buộc cập nhật bỏ qua trạng thái kho lưu trữ cục bộ.")
    update_flags.add_argument("-pip", "--pip", action="store_true",
                              help="Cài đặt/cập nhật phụ thuộc sau khi nâng cấp.")

    @commands.is_owner()
    @commands.max_concurrency(1, commands.BucketType.default)
    @commands.command(aliases=["up"], description="Cập nhật mã nguồn của tôi bằng git.",
                   emoji="<:git:944873798166020116>", alt_name="Cập nhật Bot", extras={"flags": update_flags})
    async def update(self, ctx: Union[commands.Context, disnake.MessageInteraction], *,
                     opts: str = ""):

        out_git = ""

        git_log = []

        if shutil.which("poetry"):
            file = "./pyproject.toml"
            use_poetry = True
        else:
            file = "./requirements.txt"
            use_poetry = False

        requirements_old = ""
        try:
            with open(file) as f:
                requirements_old = f.read()
        except:
            pass

        args, unknown = self.bot.get_command("update").extras['flags'].parse_known_args(opts.split())

        try:
            await ctx.response.defer()
        except:
            pass

        update_git = True
        rename_git_bak = False

        if args.force or not os.path.exists("./.git"):

            if rename_git_bak:=os.path.exists("./.gitbak") and os.environ.get("HOSTNAME") == "squarecloud.app":
                pass
            else:
                update_git = False
                out_git += await self.cleanup_git(force=args.force)

        if update_git:

            if rename_git_bak or os.environ.get("HOSTNAME") == "squarecloud.app" and os.path.isdir("./.gitbak"):
                try:
                    shutil.rmtree("./.git")
                except:
                    pass
                os.rename("./.gitbak", "./.git")

            try:
                await run_command("git reset --hard")
            except:
                pass

            try:
                pull_log = await run_command("git pull --allow-unrelated-histories -X theirs")
                if "Already up to date" in pull_log:
                    raise GenericError("**Tôi đã cài đặt bản cập nhật mới nhất...**")
                out_git += pull_log

            except GenericError as e:
                raise e

            except Exception as e:

                if "Already up to date" in str(e):
                    raise GenericError("Tôi đã cài đặt các bản cập nhật mới nhất...")

                elif not "Fast-forward" in str(e):
                    out_git += await self.cleanup_git(force=True)

                elif "Need to specify how to reconcile divergent branches" in str(e):
                    out_git += await run_command("git rebase --no-ff")

            commit = ""

            for l in out_git.split("\n"):
                if l.startswith("Updating"):
                    commit = l.replace("Updating ", "").replace("..", "...")
                    break

            data = (await run_command(f"git log {commit} {self.git_format}")).split("\n")

            git_log += format_git_log(data)

        if os.environ.get("HOSTNAME") == "squarecloud.app":
            try:
                shutil.rmtree("./.gitbak")
            except:
                pass
            shutil.copytree("./.git", "./.gitbak")

        text = "`Tôi sẽ cần phải khởi động lại sau khi thay đổi.`"

        txt = f"`✅` **[Cập nhật hoàn tất thành công!]({self.bot.pool.remote_git_url}/commits/main)**"

        if git_log:
            txt += f"\n\n{self.format_log(git_log[:10])}"

        txt += f"\n\n`📄` **Log:** ```py\n{out_git[:1000].split('Fast-forward')[-1]}```\n{text}"

        if isinstance(ctx, commands.Context):
            embed = disnake.Embed(
                description=txt,
                color=self.bot.get_color(ctx.guild.me)
            )
            await ctx.send(embed=embed, view=self.owner_view)

            self.bot.loop.create_task(self.update_deps(ctx, requirements_old, args, use_poetry=use_poetry))

        else:
            self.bot.loop.create_task(self.update_deps(ctx, requirements_old, args, use_poetry=use_poetry))
            return txt

    async def update_deps(self, ctx, original_reqs, args, use_poetry=False):

        if use_poetry:
            cmd = "poetry install"
            file = "./pyproject.toml"
        else:
            cmd = "pip3 install -U -r requirements.txt --no-cache-dir"
            file = "./requirements.txt"

        if args.pip:

            embed = disnake.Embed(
                description="**Đang cài đặt các phần phụ thuộc.\nVui lòng đợi...**",
                color=self.bot.get_color(ctx.guild.me)
            )

            msg = await ctx.channel.send(embed=embed)

            await run_command(cmd)

            embed.description = "**Các phần phụ thuộc đã được cài đặt thành công!**"

            await msg.edit(embed=embed)

        else:

            with open(file) as f:
                requirements_new = f.read()

            if original_reqs != requirements_new:

                txt = ""

                if venv:=os.getenv("VIRTUAL_ENV"):
                    if os.name == "nt":
                        txt += "call " + venv.split('\\')[-1] + " && "
                    else:
                        txt += ". ./" + venv.split('/')[-1] + " && "

                try:
                    prefix = ctx.prefix if (not str(ctx.guild.me.id) in ctx.prefix) else f"@{ctx.guild.me.name}"
                except AttributeError:
                    prefix = self.bot.default_prefix if self.bot.intents.message_content else f"@{ctx.guild.me.name}"

                await ctx.send(
                    embed=disnake.Embed(
                        description="**Bạn sẽ cần cập nhật các phần phụ thuộc bằng lệnh "
                                     "bên dưới trong thiết bị đầu cuối:**\n"
                                    f"```sh\n{txt}{cmd}```\nou usar usar o comando: "
                                    f"```ansi\n[34;1m{prefix}update --force --pip[0m``` \n"
                                    f"**Lưu ý:** Tùy thuộc vào hosting (hoặc nếu bạn không có 150mb RAM trống "
                                     f" và 0,5vCPU), bạn phải gửi tệp require.txt thay vì "
                                     f"sử dụng một trong các tùy chọn ở trên hoặc các nút cài đặt phụ thuộc bên dưới...",
                        color=self.bot.get_color(ctx.guild.me)
                    ),
                    components=[
                        disnake.ui.Button(label="Download requirements.txt", custom_id="updatecmd_requirements"),
                        disnake.ui.Button(label="Cập nhật phần phụ thuộc",
                                          custom_id="updatecmd_installdeps_" + ("poetry" if use_poetry else "pip")),
                        disnake.ui.Button(label="Cập nhật phụ thuộc (bắt buộc)",
                                          custom_id="updatecmd_installdeps_force_" + ("poetry" if use_poetry else "pip")),
                    ]
                )

    @commands.Cog.listener("on_button_click")
    async def update_buttons(self, inter: disnake.MessageInteraction):

        if not inter.data.custom_id.startswith("updatecmd_"):
            return

        if inter.data.custom_id.startswith("updatecmd_requirements"):

            try:
                os.remove('./update_reqs.zip')
            except FileNotFoundError:
                pass

            with ZipFile('update_reqs.zip', 'w') as zipObj:
                zipObj.write("requirements.txt")

            await inter.send(
                embed=disnake.Embed(
                    description="**Tải xuống tệp đính kèm và gửi nó đến máy chủ của bạn thông qua cam kết, v.v..**",
                    color=self.bot.get_color(inter.guild.me)
                ),
                file=disnake.File("update_reqs.zip")
            )

            os.remove("update_reqs.zip")
            return

        # install installdeps

        if inter.data.custom_id.startswith("updatecmd_installdeps_force_"):
            await self.cleanup_git(force=True)

        await inter.message.delete()

        args, unknown = self.bot.get_command("update").extras['flags'].parse_known_args(["-pip"])

        await self.update_deps(inter, "", args, use_poetry=inter.data.custom_id.endswith("_poetry"))

    async def cleanup_git(self, force=False):

        if force:
            try:
                shutil.rmtree("./.git")
            except FileNotFoundError:
                pass

        out_git = ""

        for c in self.git_init_cmds:
            try:
                out_git += (await run_command(c)) + "\n"
            except Exception as e:
                out_git += f"{e}\n"

        self.bot.pool.commit = (await run_command("git rev-parse HEAD")).strip("\n")
        self.bot.pool.remote_git_url = self.bot.config["SOURCE_REPO"][:-4]

        return out_git
        
def setup(bot: ClientUser):
    bot.add_cog(Owner(bot))