from pydantic_settings import BaseSettings, SettingsConfigDict

class ConsumerSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='EVENT_CONSUMER_', 
                                      case_sensitive=False,
                                      env_file=".env", 
                                      env_file_encoding='utf-8',
                                      extra="allow" )
    
    port: int = 8000
    database_url: str
    postgres_db: str
    postgres_user: str
    postgres_password: str

class PropagatorSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='EVENT_PROPAGATOR_', 
                                      case_sensitive=False,
                                      env_file=".env", 
                                      env_file_encoding='utf-8',
                                      extra="allow" )
    
    interval: int = 5
    target_url: str
    events_file: str

consumer_settings = ConsumerSettings()
propagator_settings = PropagatorSettings()