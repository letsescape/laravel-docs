# 요청 제한 (Rate Limiting)

- [소개](#introduction)
    - [캐시 설정](#cache-configuration)
- [기본 사용법](#basic-usage)
    - [시도 횟수 수동 증가](#manually-incrementing-attempts)
    - [시도 횟수 초기화](#clearing-attempts)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 애플리케이션의 [캐시](cache)와 함께 사용할 수 있는 간단한 요청 제한 추상화 기능을 제공합니다. 이를 통해 지정된 시간 동안 특정 동작을 손쉽게 제한할 수 있습니다.

> [!NOTE]
> 들어오는 HTTP 요청의 요청 제한(rate limiting)에 관심이 있으시다면, [rate limiter 미들웨어 문서](/docs/12.x/routing#rate-limiting)를 참고하시기 바랍니다.

<a name="cache-configuration"></a>
### 캐시 설정

일반적으로 요청 제한기는 애플리케이션 `cache` 설정 파일 내의 `default` 키에 정의된 기본 애플리케이션 캐시를 사용합니다. 그러나 요청 제한기에서 사용할 캐시 드라이버를 지정하려면, 애플리케이션의 `cache` 설정 파일에 `limiter` 키를 추가하여 지정할 수 있습니다:

```php
'default' => env('CACHE_STORE', 'database'),

'limiter' => 'redis', // [tl! add]
```

<a name="basic-usage"></a>
## 기본 사용법 (Basic Usage)

요청 제한기는 `Illuminate\Support\Facades\RateLimiter` 파사드를 사용하여 조작할 수 있습니다. 가장 간편하게 사용할 수 있는 메서드는 `attempt` 메서드로, 지정된 초(sec) 동안 주어진 콜백을 요청 제한합니다.

`attempt` 메서드는 더 이상 남은 시도 가능 횟수가 없으면 `false`를 반환하며, 시도 가능 횟수가 남아 있다면 콜백의 실행 결과나 `true`를 반환합니다. `attempt` 메서드의 첫 번째 인수는 요청 제한에 사용할 "키(key)"로, 제한을 적용할 특정 동작을 대표하는 임의의 문자열을 사용할 수 있습니다:

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
### 시도 횟수 수동 증가

요청 제한기를 좀 더 세밀하게 수동으로 다루고 싶다면, 다양한 메서드를 사용할 수 있습니다. 예를 들어, `tooManyAttempts` 메서드를 사용하면 특정 요청 제한 키가 1분 내 최대 허용 횟수를 초과하였는지 확인할 수 있습니다:

```php
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
    return 'Too many attempts!';
}

RateLimiter::increment('send-message:'.$user->id);

// Send message...
```

또는, `remaining` 메서드를 사용하여 특정 키의 남은 시도 가능 횟수를 조회할 수 있습니다. 남은 재시도 가능 횟수가 있다면, `increment` 메서드를 호출하여 시도 횟수를 1 증가시킬 수 있습니다:

```php
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::remaining('send-message:'.$user->id, $perMinute = 5)) {
    RateLimiter::increment('send-message:'.$user->id);

    // Send message...
}
```

특정 요청 제한 키의 값을 한 번에 여러 번 증가시키고 싶다면, `increment` 메서드에 원하는 증가 값을 전달하면 됩니다:

```php
RateLimiter::increment('send-message:'.$user->id, amount: 5);
```

<a name="determining-limiter-availability"></a>
#### 제한 가능 여부 확인

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
### 시도 횟수 초기화

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
