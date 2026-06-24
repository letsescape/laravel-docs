<!-- # Rate Limiting -->
# Rate Limiting

- [Introduction](#introduction)
    - [Cache Configuration](#cache-configuration)
- [Basic Usage](#basic-usage)
    - [Manually Incrementing Attempts](#manually-incrementing-attempts)
    - [Clearing Attempts](#clearing-attempts)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel includes a simple to use rate limiting abstraction which, in conjunction with your application's [cache](cache), provides an easy way to limit any action during a specified window of time. -->
Laravel은 애플리케이션의 [cache](/docs/8.x/cache) 기능과 연동하여, 정해진 시간 동안 특정 작업의 실행 횟수를 간편하게 제한할 수 있는 쉬운 속도 제한(rate limiting) 추상화를 제공합니다.

> [!TIP]
> 만약 외부에서 들어오는 HTTP 요청을 제한하고 싶으시다면, [rate limiter middleware documentation](/docs/8.x/routing#rate-limiting)를 참고하시기 바랍니다.

<a name="cache-configuration"></a>
<!-- ### Cache Configuration -->
### Cache Configuration

<!-- Typically, the rate limiter utilizes your default application cache as defined by the `default` key within your application's `cache` configuration file. However, you may specify which cache driver the rate limiter should use by defining a `limiter` key within your application's `cache` configuration file: -->
일반적으로 속도 제한기는 애플리케이션의 `cache` 설정 파일에서 `default` 키에 지정된 기본 캐시 드라이버를 사용합니다. 하지만, 필요한 경우 `cache` 설정 파일에 `limiter` 키를 추가해서 속도 제한에 사용할 캐시 드라이버를 명시적으로 지정할 수도 있습니다.

```
'default' => 'memcached',

'limiter' => 'redis',
```

<a name="basic-usage"></a>
<!-- ## Basic Usage -->
## Basic Usage

<!-- The `Illuminate\Support\Facades\RateLimiter` facade may be used to interact with the rate limiter. The simplest method offered by the rate limiter is the `attempt` method, which rate limits a given callback for a given number of seconds. -->
속도 제한기와 상호작용하려면 `Illuminate\Support\Facades\RateLimiter` 파사드를 사용할 수 있습니다. 속도 제한기에서 제공하는 가장 단순한 메서드는 `attempt` 메서드로, 특정 콜백이 일정 초 동안 정해진 횟수만큼 실행되도록 제한합니다.

<!-- The `attempt` method returns `false` when the callback has no remaining attempts available; otherwise, the `attempt` method will return the callback's result or `true`. The first argument accepted by the `attempt` method is a rate limiter "key", which may be any string of your choosing that represents the action being rate limited: -->
`attempt` 메서드는 남은 시도 횟수가 없으면 `false`를 반환하며, 그렇지 않다면 `attempt` 메서드는 콜백의 실행 결과 또는 `true`를 반환합니다. `attempt` 메서드의 첫 번째 인자는 속도 제한을 적용할 "키"로, 제한할 동작을 고유하게 식별할 수 있는 아무 문자열이나 사용할 수 있습니다.

```
use Illuminate\Support\Facades\RateLimiter;

$executed = RateLimiter::attempt(
    'send-message:'.$user->id,
    $perMinute = 5,
    function() {
        // Send message...
    }
);

if (! $executed) {
  return 'Too many messages sent!';
}
```

<a name="manually-incrementing-attempts"></a>
<!-- ### Manually Incrementing Attempts -->
### Manually Incrementing Attempts

<!-- If you would like to manually interact with the rate limiter, a variety of other methods are available. For example, you may invoke the `tooManyAttempts` method to determine if a given rate limiter key has exceeded its maximum number of allowed attempts per minute: -->
속도 제한기와 수동으로 상호작용하려면 다양한 메서드를 활용할 수 있습니다. 예를 들어, `tooManyAttempts` 메서드를 사용하면 특정 키에 대해 1분 내 허용된 최대 시도 횟수를 초과했는지 확인할 수 있습니다.

```
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
    return 'Too many attempts!';
}
```

<!-- Alternatively, you may use the `remaining` method to retrieve the number of attempts remaining for a given key. If a given key has retries remaining, you may invoke the `hit` method to increment the number of total attempts: -->
또는, `remaining` 메서드로 해당 키에 남아 있는 시도 횟수를 확인할 수 있습니다. 아직 시도 가능 횟수가 남아 있다면, `hit` 메서드를 사용해 시도 횟수를 직접 1 증가시킬 수 있습니다.

```
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::remaining('send-message:'.$user->id, $perMinute = 5)) {
    RateLimiter::hit('send-message:'.$user->id);

    // Send message...
}
```

<a name="determining-limiter-availability"></a>
<!-- #### Determining Limiter Availability -->
#### Determining Limiter Availability

<!-- When a key has no more attempts left, the `availableIn` method returns the number of seconds remaining until more attempts will be available: -->
더 이상 시도할 수 없는 경우, `availableIn` 메서드는 추가로 시도할 수 있을 때까지 남은 초(second) 수를 반환합니다.

```
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
    $seconds = RateLimiter::availableIn('send-message:'.$user->id);

    return 'You may try again in '.$seconds.' seconds.';
}
```

<a name="clearing-attempts"></a>
<!-- ### Clearing Attempts -->
### Clearing Attempts

<!-- You may reset the number of attempts for a given rate limiter key using the `clear` method. For example, you may reset the number of attempts when a given message is read by the receiver: -->
특정 속도 제한 키에 대한 시도 횟수를 `clear` 메서드로 초기화할 수 있습니다. 예를 들어, 메시지가 수신자에 의해 읽힐 때 시도 횟수를 리셋하도록 만들 수 있습니다.

```
use App\Models\Message;
use Illuminate\Support\Facades\RateLimiter;

/**
 * Mark the message as read.
 *
 * @param  \App\Models\Message  $message
 * @return \App\Models\Message
 */
public function read(Message $message)
{
    $message->markAsRead();

    RateLimiter::clear('send-message:'.$message->user_id);

    return $message;
}
```
