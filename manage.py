import click
from tortoise import Tortoise, run_async
from tortoise.exceptions import IntegrityError

from app.models.user import create_user
from config import DB_URL


async def _init_db(_create_db=False):
    await Tortoise.init(
        db_url=DB_URL,
        modules={'models': ['app.models']},
    )
    if _create_db:
        await Tortoise.generate_schemas()


@click.group()
def cli():
    pass


@cli.command()
def init_db():
    run_async(_init_db(_create_db=True))
    click.echo('数据库初始化成功!')


async def _add_user(**kwargs):
    await _init_db()
    try:
        user = await create_user(**kwargs)
        print('创建成功')
    except IntegrityError as e:
        click.echo(str(e))
    else:
        click.echo(f'用户：{user.name}，创建成功！  ID为: {user.id}')


@cli.command()
@click.option('--name', required=True, prompt=True)  # 如果希望命令行程序能在我们错误输入或漏掉输入的情况下，友好的提示用户，就需要用到 Click 的 prompt 功能
@click.option('--email', required=False, default='', prompt=True)
@click.option('--password', required=True, prompt=True, hide_input=True,
              confirmation_prompt=True)
def add_user(name, email, password):
    run_async(_add_user(name=name, password=password, email=email))


if __name__ == '__main__':
    cli()
