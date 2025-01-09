from hypercorn.config import Config
from hypercorn.run import run

from nanapi.settings import FASTAPI_APP, HYPERCORN_CONFIG


def main():
    config = Config()
    config.application_path = FASTAPI_APP
    for k, v in HYPERCORN_CONFIG.items():
        setattr(config, k, v)

    run(config)


if __name__ == '__main__':
    main()
