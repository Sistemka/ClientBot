from .full_proccess import process
from .search_engine import process_se

PIPELINES = {
    'full': process,
    'se': process_se
}
