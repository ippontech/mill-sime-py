from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class Setting(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=".env", env_parse_none_str="null")

    project_name: str = "Mill-sime-py"

    # Database
    db_host: str
    db_port: int | None
    db_user: str
    db_password: str
    db_name: str
    db_scheme: str

    @property
    def db_url(self) -> URL:
        return URL.create(
            drivername=self.db_scheme,
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
        )


setting = Setting()
