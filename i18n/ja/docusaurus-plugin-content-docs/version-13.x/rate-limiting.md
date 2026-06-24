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
Laravel には、アプリケーションの [cache](/docs/13.x/cache) と組み合わせて、指定された時間枠内のアクションを制限する簡単な方法を提供する、使いやすいレート制限抽象化が含まれています。

> [!NOTE]
> 受信 HTTP リクエストのレート制限に興味がある場合は、[rate limiter middleware documentation](/docs/13.x/routing#rate-limiting) を参照してください。

<a name="cache-configuration"></a>
<!-- ### Cache Configuration -->
### Cache Configuration

<!-- Typically, the rate limiter utilizes your default application cache as defined by the `default` key within your application's `cache` configuration file. However, you may specify which cache driver the rate limiter should use by defining a `limiter` key within your application's `cache` configuration file: -->
通常、レート リミッターは、アプリケーションの `cache` 構成ファイル内の `default` キーで定義されているデフォルトのアプリケーション キャッシュを利用します。ただし、アプリケーションの `cache` 構成ファイル内で `limiter` キーを定義することで、レート リミッターが使用するキャッシュ ドライバを指定できます。

```php
'default' => env('CACHE_STORE', 'database'),

'limiter' => 'redis', // [tl! add]
```

<a name="basic-usage"></a>
<!-- ## Basic Usage -->
## Basic Usage

<!-- The `Illuminate\Support\Facades\RateLimiter` facade may be used to interact with the rate limiter. The simplest method offered by the rate limiter is the `attempt` method, which rate limits a given callback for a given number of seconds. -->
`Illuminate\Support\Facades\RateLimiter` ファサードは、レート リミッターと対話するために使用できます。レート リミッターによって提供される最も単純なメソッドは `attempt` メソッドです。これは、指定された秒数の間、指定されたコールバックをレート制限します。

<!-- The `attempt` method returns `false` when the callback has no remaining attempts available; otherwise, the `attempt` method will return the callback's result or `true`. The first argument accepted by the `attempt` method is a rate limiter "key", which may be any string of your choosing that represents the action being rate limited: -->
コールバックに利用できる試行が残っていない場合、`attempt` メソッドは `false` を返します。それ以外の場合、`attempt` メソッドはコールバックの結果または `true` を返します。 `attempt` メソッドで受け入れられる最初の引数はレート リミッター「キー」です。これは、レートが制限されているアクションを表す任意の文字列を選択できます。

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
必要に応じて、`attempt` メソッドに 4 番目の引数を指定できます。これは、「減衰率」、つまり利用可能な試行回数がリセットされるまでの秒数です。たとえば、上記の例を変更して、2 分ごとに 5 回の試行を許可することができます。

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
レート リミッタを手動で操作したい場合は、他のさまざまな方法を利用できます。たとえば、`tooManyAttempts` メソッドを呼び出して、特定のレート リミッター キーが 1 分間に許可される最大試行回数を超えているかどうかを判断できます。

```php
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
    return 'Too many attempts!';
}

RateLimiter::increment('send-message:'.$user->id);

// Send message...
```

<!-- When rate limiting an endpoint that may receive many simultaneous requests, you may wish to check the value returned by the `increment` method instead of using `tooManyAttempts` and `increment` as separate operations. When using the `redis`, `memcached`, or `database` cache stores, this value is incremented atomically, ensuring each concurrent request receives a unique count: -->
多数の同時リクエストを受け取る可能性のあるエンドポイントをレート制限する場合は、`tooManyAttempts` と `increment` を別々の操作として使うのではなく、`increment` メソッドが返す値を確認するとよいでしょう。`redis`、`memcached`、`database` のキャッシュストアを使用している場合、この値はアトミックに増分されるため、同時実行される各リクエストが一意のカウントを受け取ることが保証されます。

```php
use Illuminate\Support\Facades\RateLimiter;

$perMinute = 5;

if (RateLimiter::increment('send-message:'.$user->id) > $perMinute) {
    return 'Too many attempts!';
}

// Send message...
```

<!-- Alternatively, you may use the `remaining` method to retrieve the number of attempts remaining for a given key. If a given key has retries remaining, you may invoke the `increment` method to increment the number of total attempts: -->
あるいは、`remaining` メソッドを使用して、特定のキーの残りの試行回数を取得することもできます。特定のキーに再試行が残っている場合は、`increment` メソッドを呼び出して合計試行回数を増やすことができます。

```php
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::remaining('send-message:'.$user->id, $perMinute = 5)) {
    RateLimiter::increment('send-message:'.$user->id);

    // Send message...
}
```

<!-- If you would like to increment the value for a given rate limiter key by more than one, you may provide the desired amount to the `increment` method: -->
特定のレート リミッター キーの値を 2 つ以上増分したい場合は、`increment` メソッドに必要な量を指定できます。

```php
RateLimiter::increment('send-message:'.$user->id, amount: 5);
```

<a name="determining-limiter-availability"></a>
<!-- #### Determining Limiter Availability -->
#### Determining Limiter Availability

<!-- When a key has no more attempts left, the `availableIn` method returns the number of seconds remaining until more attempts will be available: -->
キーの試行がもう残っていない場合、`availableIn` メソッドは、さらに試行が可能になるまでの残りの秒数を返します。

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
`clear` メソッドを使用して、特定のレート リミッター キーの試行回数をリセットできます。たとえば、受信者が特定のメッセージを読み取るときの試行回数をリセットできます。

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
