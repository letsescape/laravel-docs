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
Laravel には、アプリケーションの [cache](/docs/9.x/cache) と組み合わせて、指定された時間枠内のアクションを制限する簡単な方法を提供する、使いやすいレート制限抽象化が含まれています。

> [!NOTE]
> 受信 HTTP リクエストのレート制限に興味がある場合は、[rate limiter middleware documentation](/docs/9.x/routing#rate-limiting) を参照してください。

<a name="cache-configuration"></a>
<!-- ### Cache Configuration -->
### Cache Configuration

<!-- Typically, the rate limiter utilizes your default application cache as defined by the `default` key within your application's `cache` configuration file. However, you may specify which cache driver the rate limiter should use by defining a `limiter` key within your application's `cache` configuration file: -->
通常、レート リミッターは、アプリケーションの `cache` 構成ファイル内の `default` キーで定義されているデフォルトのアプリケーション キャッシュを利用します。ただし、アプリケーションの `cache` 構成ファイル内で `limiter` キーを定義することで、レート リミッターが使用するキャッシュ ドライバを指定できます。

```
'default' => 'memcached',

'limiter' => 'redis',
```

<a name="basic-usage"></a>
<!-- ## Basic Usage -->
## Basic Usage

<!-- The `Illuminate\Support\Facades\RateLimiter` facade may be used to interact with the rate limiter. The simplest method offered by the rate limiter is the `attempt` method, which rate limits a given callback for a given number of seconds. -->
`Illuminate\Support\Facades\RateLimiter` ファサードは、レート リミッターと対話するために使用できます。レート リミッターによって提供される最も単純なメソッドは `attempt` メソッドです。これは、指定された秒数の間、指定されたコールバックをレート制限します。

<!-- The `attempt` method returns `false` when the callback has no remaining attempts available; otherwise, the `attempt` method will return the callback's result or `true`. The first argument accepted by the `attempt` method is a rate limiter "key", which may be any string of your choosing that represents the action being rate limited: -->
コールバックに利用できる試行が残っていない場合、`attempt` メソッドは `false` を返します。それ以外の場合、`attempt` メソッドはコールバックの結果または `true` を返します。 `attempt` メソッドで受け入れられる最初の引数はレート リミッター「キー」です。これは、レートが制限されているアクションを表す任意の文字列を選択できます。

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
レート リミッタを手動で操作したい場合は、他のさまざまな方法を利用できます。たとえば、`tooManyAttempts` メソッドを呼び出して、特定のレート リミッター キーが 1 分間に許可される最大試行回数を超えているかどうかを判断できます。

```
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
    return 'Too many attempts!';
}
```

<!-- Alternatively, you may use the `remaining` method to retrieve the number of attempts remaining for a given key. If a given key has retries remaining, you may invoke the `hit` method to increment the number of total attempts: -->
あるいは、`remaining` メソッドを使用して、特定のキーの残りの試行回数を取得することもできます。特定のキーに再試行が残っている場合は、`hit` メソッドを呼び出して合計試行回数を増やすことができます。

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
キーの試行がもう残っていない場合、`availableIn` メソッドは、さらに試行が可能になるまでの残りの秒数を返します。

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
`clear` メソッドを使用して、特定のレート リミッター キーの試行回数をリセットできます。たとえば、受信者が特定のメッセージを読み取るときの試行回数をリセットできます。

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
