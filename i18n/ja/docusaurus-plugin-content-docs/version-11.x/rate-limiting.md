# レート制限 (Rate Limiting)

- [Introduction](#introduction)
    - [キャッシュ構成](#cache-configuration)
- [基本的な使い方](#basic-usage)
    - [手動で試行を増やす](#manually-incrementing-attempts)
    - [クリア試行](#clearing-attempts)

<a name="introduction"></a>
## 導入 (Introduction)

Laravel には、アプリケーションの [cache](cache) と組み合わせて、指定された時間枠内のアクションを制限する簡単な方法を提供する、使いやすいレート制限抽象化が含まれています。

> [!NOTE]  
> 受信 HTTP リクエストのレート制限に興味がある場合は、[レート リミッタ ミドルウェアのドキュメント](/docs/{{version}}/routing#rate-limiting) を参照してください。

<a name="cache-configuration"></a>
### キャッシュ構成

通常、レート リミッターは、アプリケーションの `cache` 構成ファイル内の `default` キーで定義されているデフォルトのアプリケーション キャッシュを利用します。ただし、アプリケーションの `cache` 構成ファイル内で `limiter` キーを定義することで、レート リミッターが使用するキャッシュ ドライバを指定できます。

    'default' => env('CACHE_STORE', 'database'),

    'limiter' => 'redis',

<a name="basic-usage"></a>
## 基本的な使い方 (Basic Usage)

`Illuminate\Support\Facades\RateLimiter` ファサードは、レート リミッターと対話するために使用できます。レート リミッターによって提供される最も単純なメソッドは `attempt` メソッドです。これは、指定された秒数の間、指定されたコールバックをレート制限します。

コールバックに利用できる試行が残っていない場合、`attempt` メソッドは `false` を返します。それ以外の場合、`attempt` メソッドはコールバックの結果または `true` を返します。 `attempt` メソッドで受け入れられる最初の引数はレート リミッター「キー」です。これは、レートが制限されているアクションを表す任意の文字列を選択できます。

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

必要に応じて、`attempt` メソッドに 4 番目の引数を指定できます。これは、「減衰率」、つまり利用可能な試行回数がリセットされるまでの秒数です。たとえば、上記の例を変更して、2 分ごとに 5 回の試行を許可することができます。

    $executed = RateLimiter::attempt(
        'send-message:'.$user->id,
        $perTwoMinutes = 5,
        function() {
            // Send message...
        },
        $decayRate = 120,
    );

<a name="manually-incrementing-attempts"></a>
### 手動で試行を増やす

レート リミッタを手動で操作したい場合は、他のさまざまな方法を利用できます。たとえば、`tooManyAttempts` メソッドを呼び出して、特定のレート リミッター キーが 1 分間に許可される最大試行回数を超えているかどうかを判断できます。

    use Illuminate\Support\Facades\RateLimiter;

    if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
        return 'Too many attempts!';
    }

    RateLimiter::increment('send-message:'.$user->id);

    // Send message...

あるいは、`remaining` メソッドを使用して、特定のキーの残りの試行回数を取得することもできます。特定のキーに再試行が残っている場合は、`increment` メソッドを呼び出して合計試行回数を増やすことができます。

    use Illuminate\Support\Facades\RateLimiter;

    if (RateLimiter::remaining('send-message:'.$user->id, $perMinute = 5)) {
        RateLimiter::increment('send-message:'.$user->id);

        // Send message...
    }

特定のレート リミッター キーの値を 2 つ以上増分したい場合は、`increment` メソッドに必要な量を指定できます。

    RateLimiter::increment('send-message:'.$user->id, amount: 5);

<a name="determining-limiter-availability"></a>
#### リミッターの可用性の決定

キーの試行がもう残っていない場合、`availableIn` メソッドは、さらに試行が可能になるまでの残りの秒数を返します。

    use Illuminate\Support\Facades\RateLimiter;

    if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
        $seconds = RateLimiter::availableIn('send-message:'.$user->id);

        return 'You may try again in '.$seconds.' seconds.';
    }

    RateLimiter::increment('send-message:'.$user->id);

    // Send message...

<a name="clearing-attempts"></a>
### クリア試行

`clear` メソッドを使用して、特定のレート リミッター キーの試行回数をリセットできます。たとえば、受信者が特定のメッセージを読み取るときの試行回数をリセットできます。

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

