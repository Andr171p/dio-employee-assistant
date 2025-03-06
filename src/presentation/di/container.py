from dishka import make_async_container

from src.presentation.di.providers import RAGProvider


container = make_async_container(RAGProvider())
