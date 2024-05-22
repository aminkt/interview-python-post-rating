import logging
import threading
import signal
import sys

from django.core.management.base import BaseCommand

from project.dependencies import Dependencies

class Command(BaseCommand):
    help = 'Update post rate count and score sum'

    def __init__(self):
        super().__init__()
        self.lock = threading.Lock()
        self.shutdown_flag = threading.Event()
        self.__num_threads = 5

    def handle(self, *args, **kwargs):
        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.shutdown_handler)
        signal.signal(signal.SIGTERM, self.shutdown_handler)

        self.apply_delayed_posts()

    def shutdown_handler(self, signum, frame):
        self.stdout.write(self.style.WARNING('Received termination signal. Waiting for threads to finish...'))
        self.shutdown_flag.set()

    def process_batch(self, rate_ids):
        is_done = False
        while not self.shutdown_flag.is_set() and not is_done:
            try:
                Dependencies.rating_repository().apply_pending_rates(rate_ids)
                is_done = True
            except Exception as e:
                logging.exception(e)
                self.stderr.write(f"Error processing rates {rate_ids}: {e}")

    def apply_delayed_posts(self):
        page = 1
        while not self.shutdown_flag.is_set():
            rate_ids = Dependencies.rating_repository().get_queued_rate_ids(page)
            if len(rate_ids) == 0:
                break
            else:
                page += 1

            # Find post ids which has unprocessed rates.
            if len(rate_ids) <= 100:
                chunk_size = len(rate_ids)
            else:
                chunk_size = len(rate_ids) // self.__num_threads

            threads = []
            # Chunk post ids in different threads to handle them in parallel.
            for i in range(self.__num_threads):
                start = i * chunk_size
                end = (i + 1) * chunk_size if i != self.__num_threads - 1 else len(rate_ids)
                chunked_rate_ids = rate_ids[start:end]
                if chunked_rate_ids:
                    thread = threading.Thread(target=self.process_batch, args=(chunked_rate_ids,))
                    threads.append(thread)
                    thread.start()
                    self.stdout.write(f'Thread {i+1} started to handle {len(chunked_rate_ids)} items.')
                else:
                    self.stdout.write(f'Empty chunk for thread {i+1}. stop creating new thread.')

            # Wait for all threads to complete or for shutdown signal
            for thread in threads:
                thread.join()

            if self.shutdown_flag.is_set():
                self.stderr.write(self.style.WARNING(f'Graceful shutdown completed. (in page {page-1}) Exiting...'))
                sys.exit(0)
            else:
                self.stdout.write(
                    self.style.SUCCESS(f'Post rate_count and score_sum updated successfully. (in page {page-1})'))

        self.stdout.write(self.style.SUCCESS(f'All pending items calculated in {page-1} page'))
