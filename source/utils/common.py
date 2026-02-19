import subprocess
import time
from functools import wraps


def retry(max_attempts=3, delay=3, backoff=2, exceptions=(Exception,)):
    """
    Decorator that retries a function call upon specified exceptions.
    
    Parameters:
        max_attempts (int): Maximum number of retry attempts.
        delay (int or float): Initial delay in seconds before the first retry.
        backoff (int or float): Multiplier applied to the delay after each failed attempt.
        exceptions (tuple): Tuple of exception classes that trigger a retry.
    
    Returns:
        function: The decorated function with retry logic applied.
    
    Raises:
        The last exception encountered if all retry attempts fail.
    """

    def decorator(func):
        """
        Decorator that retries a function call upon specified exceptions up to a maximum number of attempts.
        
        If the decorated function raises an exception listed in `exceptions`, it will be retried after a delay, with the delay increasing by the `backoff` multiplier after each attempt. If the maximum number of attempts is reached, the exception is re-raised.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            current_delay = delay

            while attempt < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    error_type = type(e).__name__
                    if attempt >= max_attempts:
                        print(f"최대 시도 횟수 초과. 오류: {error_type} - {e}")
                        raise

                    print(f"재시도 중... ({attempt}/{max_attempts})")
                    time.sleep(current_delay)
                    current_delay *= backoff

        return wrapper

    return decorator


def timeout(seconds=600):
    """
    Decorator that enforces a time limit on the execution of the decorated function.
    
    Parameters:
        seconds (int): Maximum allowed execution time in seconds before raising a TimeoutError.
    
    Raises:
        TimeoutError: If the decorated function exceeds the specified execution time.
    """

    def decorator(func):
        """
        Decorator that enforces a time limit on the execution of the decorated function.
        
        If the function does not complete within the specified number of seconds, a TimeoutError is raised.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            import signal

            def handler(signum, frame):
                raise TimeoutError(f"함수 실행이 {seconds}초를 초과했습니다.")

            # 타임아웃 설정
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(seconds)

            try:
                result = func(*args, **kwargs)
                signal.alarm(0)  # 타이머 재설정
                return result
            except TimeoutError:
                raise
            finally:
                signal.alarm(0)  # 타이머 재설정

        return wrapper

    return decorator


def run_command(command, cwd=None):
    """명령어를 실행하고 결과를 반환

    Args:
        command: 실행할 명령어
        cwd: 명령어를 실행할 디렉토리 (기본값: None)

    Returns:
        str: 명령어 실행 결과
    """
    result = subprocess.run(
        command,
        shell=True,
        check=True,
        text=True,
        capture_output=True,
        cwd=cwd
    )
    return result.stdout.strip()
