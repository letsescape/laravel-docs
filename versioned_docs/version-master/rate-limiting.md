# 요청 제한 (Rate Limiting)

- [소개](#introduction)
    - [캐시 설정](#cache-configuration)
- [기본 사용법](#basic-usage)
    - [시도 횟수 수동 증가](#manually-incrementing-attempts)
    - [시도 횟수 초기화](#clearing-attempts)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 사용하기 쉬운 요청 제한 추상화 기능을 제공합니다. 이 기능은 애플리케이션의 [캐시](cache)와 결합하여, 지정된 시간 동안 특정 동작을 쉽게 제한할 수 있도록 해줍니다.

> [!NOTE]
> 들어오는 HTTP 요청에 대한 요청 제한이 궁금하시다면, [요청 제한 미들웨어 문서](/docs/master/routing#rate-limiting)를 참고하시기 바랍니다.

<a name="cache-configuration"></a>
### 캐시 설정 (Cache Configuration)

일반적으로 요청 제한은 애플리케이션의 `cache` 설정 파일에 있는 `default` 키에 정의된 기본 캐시를 사용합니다. 하지만, 요청 제한에서 사용할 캐시 드라이버를 별도로 지정하고 싶다면, 애플리케이션의 `cache` 설정 파일에 `limiter` 키를 추가하여 지정할 수 있습니다:

```php
'default' => env('CACHE_STORE', 'database'),

'limiter' => 'redis', // [tl! add]
```

<a name="basic-usage"></a>
## 기본 사용법 (Basic Usage)

`Illuminate\Support\Facades\RateLimiter` 파사드(facade)를 사용하면 요청 제한 기능에 접근할 수 있습니다. 요청 제한 기능이 제공하는 가장 간단한 메서드는 `attempt` 메서드로, 특정 콜백을 지정한 초 단위 시간 동안 제한할 수 있습니다.

`attempt` 메서드는 남은 시도 가능 횟수가 없을 때 `false`를 반환하며, 그 외에는 콜백의 결과 또는 `true`를 반환합니다. `attempt` 메서드의 첫 번째 인수는 요청 제한의 "키"이며, 이는 제한하려는 동작을 식별할 수 있는 어떤 문자열이든 사용할 수 있습니다:

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

필요하다면, `attempt` 메서드에 네 번째 인수로 "감쇠 시간(decay rate)"을 추가로 전달할 수 있습니다. 이 값은 사용 가능한 시도 횟수가 리셋되는 데 걸리는 초(second) 단위의 시간입니다. 예를 들어, 위의 예시를 수정하여 2분마다 5번의 시도를 허용할 수 있습니다:

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
### 시도 횟수 수동 증가

요청 제한 기능을 수동으로 제어하고 싶다면 다양한 다른 메서드도 사용할 수 있습니다. 예를 들어, `tooManyAttempts` 메서드를 사용하여 특정 요청 제한 키가 분당 허용된 최대 시도 횟수를 초과했는지 판단할 수 있습니다:

```php
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
    return 'Too many attempts!';
}

RateLimiter::increment('send-message:'.$user->id);

// Send message...
```

또는, `remaining` 메서드를 사용하여 주어진 키의 남은 시도 가능 횟수를 확인할 수 있습니다. 시도 가능 횟수가 남아 있다면, `increment` 메서드로 총 시도 횟수를 증가시킬 수 있습니다:

```php
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::remaining('send-message:'.$user->id, $perMinute = 5)) {
    RateLimiter::increment('send-message:'.$user->id);

    // Send message...
}
```

특정 요청 제한 키의 값을 한 번에 여러 번 증가시키고 싶다면, `increment` 메서드에 원하는 증가량을 지정하여 사용할 수 있습니다:

```php
RateLimiter::increment('send-message:'.$user->id, amount: 5);
```

<a name="determining-limiter-availability"></a>
#### 제한 가능 여부 확인

키에 더 이상 남은 시도 횟수가 없을 때, `availableIn` 메서드는 다음 시도가 가능해질 때까지 남은 초(second) 단위의 시간을 반환합니다:

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
### 시도 횟수 초기화 (Clearing Attempts)

`clear` 메서드를 사용하면 특정 요청 제한 키의 시도 횟수를 초기화할 수 있습니다. 예를 들어, 특정 메시지가 받는 사람에 의해 읽혔을 때 시도 횟수를 초기화할 수 있습니다:

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
