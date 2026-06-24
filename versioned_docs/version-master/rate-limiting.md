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
Laravel은 애플리케이션의 [cache](/docs/master/cache)와 함께 사용할 수 있는 간단한 요청 제한 추상화 기능을 제공합니다. 이를 통해 지정된 시간 동안 특정 동작을 손쉽게 제한할 수 있습니다.

> [!NOTE]
> 들어오는 HTTP 요청의 요청 제한(rate limiting)에 관심이 있으시다면, [rate limiter middleware documentation](/docs/master/routing#rate-limiting)를 참고하시기 바랍니다.

<a name="cache-configuration"></a>
<!-- ### Cache Configuration -->
### Cache Configuration

<!-- Typically, the rate limiter utilizes your default application cache as defined by the `default` key within your application's `cache` configuration file. However, you may specify which cache driver the rate limiter should use by defining a `limiter` key within your application's `cache` configuration file: -->
일반적으로 요청 제한기는 애플리케이션 `cache` 설정 파일 내의 `default` 키에 정의된 기본 애플리케이션 캐시를 사용합니다. 그러나 요청 제한기에서 사용할 캐시 드라이버를 지정하려면, 애플리케이션의 `cache` 설정 파일에 `limiter` 키를 추가하여 지정할 수 있습니다:

```php
'default' => env('CACHE_STORE', 'database'),

'limiter' => 'redis', // [tl! add]
```

<a name="basic-usage"></a>
<!-- ## Basic Usage -->
## Basic Usage

<!-- The `Illuminate\Support\Facades\RateLimiter` facade may be used to interact with the rate limiter. The simplest method offered by the rate limiter is the `attempt` method, which rate limits a given callback for a given number of seconds. -->
요청 제한기는 `Illuminate\Support\Facades\RateLimiter` 파사드를 사용하여 조작할 수 있습니다. 가장 간편하게 사용할 수 있는 메서드는 `attempt` 메서드로, 지정된 초(sec) 동안 주어진 콜백을 요청 제한합니다.

<!-- The `attempt` method returns `false` when the callback has no remaining attempts available; otherwise, the `attempt` method will return the callback's result or `true`. The first argument accepted by the `attempt` method is a rate limiter "key", which may be any string of your choosing that represents the action being rate limited: -->
`attempt` 메서드는 더 이상 남은 시도 가능 횟수가 없으면 `false`를 반환하며, 그렇지 않으면 `attempt` 메서드는 콜백의 실행 결과나 `true`를 반환합니다. `attempt` 메서드의 첫 번째 인수는 요청 제한에 사용할 "키(key)"로, 제한을 적용할 특정 동작을 대표하는 임의의 문자열을 사용할 수 있습니다:

```php
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
필요하다면, `attempt` 메서드의 네 번째 인수로 "갱신 주기(decay rate)"를 지정할 수 있습니다. 이는 제한 횟수가 초기화되기까지 남은 초(sec)를 의미합니다. 예를 들어, 위 예제에서 2분(120초) 동안 총 5회 시도할 수 있도록 수정할 수 있습니다:

```php
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
요청 제한기를 좀 더 세밀하게 수동으로 다루고 싶다면, 다양한 메서드를 사용할 수 있습니다. 예를 들어, `tooManyAttempts` 메서드를 사용하면 특정 요청 제한 키가 1분 내 최대 허용 횟수를 초과하였는지 확인할 수 있습니다:

```php
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
    return 'Too many attempts!';
}

RateLimiter::increment('send-message:'.$user->id);

// Send message...
```

<!-- Alternatively, you may use the `remaining` method to retrieve the number of attempts remaining for a given key. If a given key has retries remaining, you may invoke the `increment` method to increment the number of total attempts: -->
또는, `remaining` 메서드를 사용하여 특정 키의 남은 시도 가능 횟수를 조회할 수 있습니다. 남은 재시도 가능 횟수가 있다면, `increment` 메서드를 호출하여 시도 횟수를 1 증가시킬 수 있습니다:

```php
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::remaining('send-message:'.$user->id, $perMinute = 5)) {
    RateLimiter::increment('send-message:'.$user->id);

    // Send message...
}
```

<!-- If you would like to increment the value for a given rate limiter key by more than one, you may provide the desired amount to the `increment` method: -->
특정 요청 제한 키의 값을 한 번에 여러 번 증가시키고 싶다면, `increment` 메서드에 원하는 증가 값을 전달하면 됩니다:

```php
RateLimiter::increment('send-message:'.$user->id, amount: 5);
```

<a name="determining-limiter-availability"></a>
<!-- #### Determining Limiter Availability -->
#### Determining Limiter Availability

<!-- When a key has no more attempts left, the `availableIn` method returns the number of seconds remaining until more attempts will be available: -->
키에 더 이상 남은 시도 횟수가 없을 때, `availableIn` 메서드는 시도 가능 횟수가 다시 초기화(재시작)되기까지 남은 초를 반환합니다:

```php
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
특정 요청 제한 키에 대한 시도 횟수를 `clear` 메서드를 사용하여 초기화할 수 있습니다. 예를 들어, 특정 메시지를 수신자가 읽었을 때 시도 횟수를 초기화할 수도 있습니다:

```php
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
