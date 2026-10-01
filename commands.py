import asyncio
import shlex



async def run_command(command: str | list[str]):

    if isinstance(command, str):
        args = shlex.split(command)
    else:
        args = command

    updates_abailable = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    stdout, _ = await updates_abailable.communicate()
    # print(f"Return code: {updates_abailable.returncode}")

    return stdout.decode().splitlines()


# asyncio.run(run_command())
