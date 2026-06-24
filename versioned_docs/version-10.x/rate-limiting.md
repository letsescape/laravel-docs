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
Laravel에서는 애플리케이션의 [cache](/docs/10.x/cache)와 함께 사용할 수 있는 단순한 요청 제한(rate limiting) 추상화 기능을 제공합니다. 이를 통해 지정한 시간 동안 어떤 작업이 허용되는지 손쉽게 제한할 수 있습니다.

> [!NOTE]
> 만약 외부에서 들어오는 HTTP 요청에 대한 속도 제한이 궁금하다면, [rate limiter middleware documentation](/docs/10.x/routing#rate-limiting)를 참고하시기 바랍니다.

<a name="cache-configuration"></a>
<!-- ### Cache Configuration -->
### Cache Configuration

<!-- Typically, the rate limiter utilizes your default application cache as defined by the `default` key within your application's `cache` configuration file. However, you may specify which cache driver the rate limiter should use by defining a `limiter` key within your application's `cache` configuration file: -->
일반적으로 요청 제한 기능은 애플리케이션의 `cache` 설정 파일 내 `default` 키에 정의된 기본 캐시 드라이버를 사용합니다. 하지만 요청 제한 기능이 사용할 캐시 드라이버를 직접 지정하고 싶다면, 애플리케이션의 `cache` 설정 파일에 `limiter` 키를 정의하면 됩니다.

```
'default' => 'memcached',

'limiter' => 'redis',
```

<a name="basic-usage"></a>
<!-- ## Basic Usage -->
## Basic Usage

<!-- The `Illuminate\Support\Facades\RateLimiter` facade may be used to interact with the rate limiter. The simplest method offered by the rate limiter is the `attempt` method, which rate limits a given callback for a given number of seconds. -->
`Illuminate\Support\Facades\RateLimiter` 파사드를 사용하여 요청 제한 기능과 상호작용할 수 있습니다. 요청 제한 기능에서 가장 간단하게 사용할 수 있는 메서드는 `attempt`입니다. 이 메서드는 주어진 콜백을 지정한 초(seconds) 동안 실행 횟수를 제한합니다.

<!-- The `attempt` method returns `false` when the callback has no remaining attempts available; otherwise, the `attempt` method will return the callback's result or `true`. The first argument accepted by the `attempt` method is a rate limiter "key", which may be any string of your choosing that represents the action being rate limited: -->
`attempt` 메서드는 해당 콜백에 남아 있는 실행 가능 횟수가 없다면 `false`를 반환합니다. 그렇지 않으면 `attempt` 메서드는 콜백의 반환값 혹은 `true`를 반환합니다. `attempt` 메서드의 첫 번째 인수는 제한을 적용할 "키"로, 제한할 동작을 식별할 수 있는 임의의 문자열을 지정할 수 있습니다.

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

<!-- If necessary, you may provide a fourth argument to the `attempt` method, which is the "decay rate", or the number of seconds until the available attempts are reset. For example, we can modify the example above to allow five attempts every two minutes: -->
필요하다면 `attempt` 메서드에 네 번째 인수를 추가할 수 있습니다. 이 네 번째 인수는 "만료 시간(decay rate)"으로, 사용할 수 있는 시도 횟수가 초기화될 때까지의 초(seconds)를 의미합니다. 예를 들어, 위 예시를 2분(120초)마다 5번 시도 가능한 형태로 수정할 수 있습니다.

```
$executed = RateLimiter::attempt(
    'send-message:'.$user->id,
    $perTwoMinutes = 5,
    function() {
        // Send message...
    },
    $decayRate = 120,
);
```

<a name="manually-incrementing-attempts"></a>
<!-- ### Manually Incrementing Attempts -->
### Manually Incrementing Attempts

<!-- If you would like to manually interact with the rate limiter, a variety of other methods are available. For example, you may invoke the `tooManyAttempts` method to determine if a given rate limiter key has exceeded its maximum number of allowed attempts per minute: -->
요청 제한 기능을 직접 제어하고 싶을 때 사용할 수 있는 다양한 메서드가 있습니다. 예를 들어, `tooManyAttempts` 메서드를 사용하면 특정 제한 키가 분당 허용된 최대 시도 횟수를 초과했는지 확인할 수 있습니다.

```
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
    return 'Too many attempts!';
}

RateLimiter::increment('send-message:'.$user->id);

// Send message...
```

<!-- Alternatively, you may use the `remaining` method to retrieve the number of attempts remaining for a given key. If a given key has retries remaining, you may invoke the `increment` method to increment the number of total attempts: -->
또는, `remaining` 메서드를 사용해 특정 키의 남은 시도 가능 횟수를 가져올 수 있습니다. 시도 가능 횟수가 있다면, `increment` 메서드를 직접 호출해서 시도 횟수를 증가시킬 수 있습니다.

```
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::remaining('send-message:'.$user->id, $perMinute = 5)) {
    RateLimiter::increment('send-message:'.$user->id);

    // Send message...
}
```

<!-- If you would like to increment the value for a given rate limiter key by more than one, you may provide the desired amount to the `increment` method: -->
또한, 만약 한 번에 1 이상으로 시도 횟수를 증가시키고 싶다면, `increment` 메서드에 원하는 증가값을 지정할 수 있습니다.

```
RateLimiter::increment('send-message:'.$user->id, amount: 5);
```

<a name="determining-limiter-availability"></a>
<!-- #### Determining Limiter Availability -->
#### Determining Limiter Availability

<!-- When a key has no more attempts left, the `availableIn` method returns the number of seconds remaining until more attempts will be available: -->
시도 횟수가 모두 소진된 경우에는 `availableIn` 메서드를 사용해 추가 시도가 가능해지기까지 남은 초(seconds)를 확인할 수 있습니다.

```
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
    $seconds = RateLimiter::availableIn('send-message:'.$user->id);

    return 'You may try again in '.$seconds.' seconds.';
}

RateLimiter::increment('send-message:'.$user->id);

// Send message...
```

<a name="clearing-attempts"></a>
<!-- ### Clearing Attempts -->
### Clearing Attempts

<!-- You may reset the number of attempts for a given rate limiter key using the `clear` method. For example, you may reset the number of attempts when a given message is read by the receiver: -->
`clear` 메서드를 사용하면 특정 제한 키의 시도 횟수를 초기화할 수 있습니다. 예를 들어, 메시지를 수신자가 읽었을 때 시도 횟수를 리셋하고 싶다면 다음과 같이 할 수 있습니다.

```
use App\Models\Message;
use Illuminate\Support\Facades\RateLimiter;

/**
 * Mark the message as read.
 */
public function read(Message $message): Message
{
    $message->markAsRead();

    RateLimiter::clear('send-message:'.$message->user_id);

    return $message;
}
```
