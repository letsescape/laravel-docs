# HTTPセッション (HTTP Session)

- [Introduction](#introduction)
    - [Configuration](#configuration)
    - [ドライバの前提条件](#driver-prerequisites)
- [セッションとの対話](#interacting-with-the-session)
    - [データの取得](#retrieving-data)
    - [データの保存](#storing-data)
    - [フラッシュデータ](#flash-data)
    - [データの削除](#deleting-data)
    - [セッションIDの再生成](#regenerating-the-session-id)
- [セッションのブロック](#session-blocking)
- [カスタムセッションドライバの追加](#adding-custom-session-drivers)
    - [ドライバの実装](#implementing-the-driver)
    - [ドライバを登録する](#registering-the-driver)

<a name="introduction"></a>
## 導入 (Introduction)

HTTP 駆動のアプリケーションはステートレスであるため、セッションは複数のリクエストにわたってユーザーに関する情報を保存する方法を提供します。そのユーザー情報は通常、後続のリクエストからアクセスできる永続ストア/バックエンドに配置されます。

Laravel には、表現力豊かな統合 API を通じてアクセスされるさまざまなセッション バックエンドが付属しています。 [Memcached](https://memcached.org)、[Redis](https://redis.io) などの一般的なバックエンドやデータベースのサポートが含まれています。

<a name="configuration"></a>
### 構成

アプリケーションのセッション構成ファイルは、`config/session.php` に保存されます。このファイルで使用できるオプションを必ず確認してください。デフォルトでは、Laravel は `file` セッションドライバを使用するように構成されており、多くのアプリケーションで適切に機能します。アプリケーションが複数の Web サーバー間で負荷分散される場合は、Redis やデータベースなど、すべてのサーバーがアクセスできる集中ストアを選択する必要があります。

session `driver` 構成オプションは、各リクエストのセッション データが保存される場所を定義します。 Laravel には、すぐに使用できるいくつかの優れたドライバが同梱されています。

<div class="content-list" markdown="1">

- `file` - セッションは `storage/framework/sessions` に保存されます。
- `cookie` - セッションは安全な暗号化された Cookie に保存されます。
- `database` - セッションはリレーショナル データベースに保存されます。
- `memcached` / `redis` - セッションは、これらの高速なキャッシュ ベースのストアのいずれかに保存されます。
- `dynamodb` - セッションは AWS DynamoDB に保存されます。
- `array` - セッションは PHP 配列に保存され、永続化されません。

</div>

> **注記**
> アレイ ドライバは主に [testing](/docs/{{version}}/testing) 中に使用され、セッションに保存されたデータが永続化されるのを防ぎます。

<a name="driver-prerequisites"></a>
### ドライバの前提条件

<a name="database"></a>
#### データベース

`database` セッション ドライバを使用する場合は、セッション レコードを含むテーブルを作成する必要があります。テーブルの `Schema` 宣言の例を以下に示します。

    Schema::create('sessions', function ($table) {
        $table->string('id')->primary();
        $table->foreignId('user_id')->nullable()->index();
        $table->string('ip_address', 45)->nullable();
        $table->text('user_agent')->nullable();
        $table->text('payload');
        $table->integer('last_activity')->index();
    });

`session:table` Artisan コマンドを使用して、この移行を生成できます。データベース移行の詳細については、完全な [移行ドキュメント](/docs/{{version}}/migrations) を参照してください。

```shell
php artisan session:table

php artisan migrate
```

<a name="redis"></a>
#### レディス

Laravel で Redis セッションを使用する前に、PECL 経由で PhpRedis PHP 拡張機能をインストールするか、Composer 経由で `predis/predis` パッケージ (~1.0) をインストールする必要があります。 Redis の構成の詳細については、Laravel の [Redis のドキュメント](/docs/{{version}}/redis#configuration) を参照してください。

> **注記**
> `session` 構成ファイルでは、`connection` オプションを使用して、セッションで使用される Redis 接続を指定できます。

<a name="interacting-with-the-session"></a>
## セッションとの対話 (Interacting With The Session)

<a name="retrieving-data"></a>
### データの取得

Laravel でセッション データを操作するには、主に 2 つの方法があります。グローバル `session` ヘルパを使用する方法と、`Request` インスタンスを使用する方法です。まず、`Request` インスタンスを介してセッションにアクセスする方法を見てみましょう。これは、ルート クロージャまたはコントローラ メソッドでタイプヒントを指定できます。コントローラメソッドの依存関係は、Laravel [サービスコンテナ](/docs/{{version}}/container) 経由で自動的に挿入されることに注意してください。

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use Illuminate\Http\Request;

    class UserController extends Controller
    {
        /**
         * Show the profile for the given user.
         *
         * @param  Request  $request
         * @param  int  $id
         * @return Response
         */
        public function show(Request $request, $id)
        {
            $value = $request->session()->get('key');

            //
        }
    }

セッションから項目を取得するときは、`get` メソッドの 2 番目の引数としてデフォルト値を渡すこともできます。指定されたキーがセッションに存在しない場合、このデフォルト値が返されます。クロージャをデフォルト値として `get` メソッドに渡し、要求されたキーが存在しない場合、クロージャが実行され、その結果が返されます。

    $value = $request->session()->get('key', 'default');

    $value = $request->session()->get('key', function () {
        return 'default';
    });

<a name="the-global-session-helper"></a>
#### グローバルセッションヘルパ

グローバル `session` PHP 関数を使用して、セッション内のデータを取得および保存することもできます。 `session` ヘルパが単一の文字列引数で呼び出されると、そのセッション キーの値が返されます。キーと値のペアの配列を使用してヘルパが呼び出される場合、それらの値はセッションに保存されます。

    Route::get('/home', function () {
        // Retrieve a piece of data from the session...
        $value = session('key');

        // Specifying a default value...
        $value = session('key', 'default');

        // Store a piece of data in the session...
        session(['key' => 'value']);
    });

> **注記**
> HTTP リクエスト インスタンス経由でセッションを使用する場合と、グローバル `session` ヘルパを使用する場合には、実質的な違いはほとんどありません。どちらのメソッドも、すべてのテスト ケースで使用できる `assertSessionHas` メソッドを介した [testable](/docs/{{version}}/testing) です。

<a name="retrieving-all-session-data"></a>
#### すべてのセッション データの取得

セッション内のすべてのデータを取得したい場合は、`all` メソッドを使用できます。

    $data = $request->session()->all();

<a name="determining-if-an-item-exists-in-the-session"></a>
#### 項目がセッション内に存在するかどうかを確認する

項目がセッションに存在するかどうかを確認するには、`has` メソッドを使用できます。項目が存在し、`null` ではない場合、`has` メソッドは `true` を返します。

    if ($request->session()->has('users')) {
        //
    }

アイテムがセッションに存在するかどうかを確認するには、その値が `null` であっても、`exists` メソッドを使用できます。

    if ($request->session()->exists('users')) {
        //
    }

項目がセッション内に存在しないかどうかを確認するには、`missing` メソッドを使用できます。項目が存在しない場合、`missing` メソッドは `true` を返します。

    if ($request->session()->missing('users')) {
        //
    }

<a name="storing-data"></a>
### データの保存

セッションにデータを保存するには、通常、リクエスト インスタンスの `put` メソッドまたはグローバル `session` ヘルパを使用します。

    // Via a request instance...
    $request->session()->put('key', 'value');

    // Via the global "session" helper...
    session(['key' => 'value']);

<a name="pushing-to-array-session-values"></a>
#### 配列セッション値へのプッシュ

`push` メソッドは、配列であるセッション値に新しい値をプッシュするために使用できます。たとえば、`user.teams` キーにチーム名の配列が含まれている場合、次のように新しい値を配列にプッシュできます。

    $request->session()->push('user.teams', 'developers');

<a name="retrieving-deleting-an-item"></a>
#### アイテムの取得と削除

`pull` メソッドは、単一のステートメントでセッションから項目を取得して削除します。

    $value = $request->session()->pull('key', 'default');

<a name="incrementing-and-decrementing-session-values"></a>
#### セッション値の増減

セッション データに増加または減少させたい整数が含まれている場合は、`increment` メソッドと `decrement` メソッドを使用できます。

    $request->session()->increment('count');

    $request->session()->increment('count', $incrementBy = 2);

    $request->session()->decrement('count');

    $request->session()->decrement('count', $decrementBy = 2);

<a name="flash-data"></a>
### フラッシュデータ

場合によっては、次のリクエストに備えてセッションに項目を保存したい場合があります。これは、`flash` メソッドを使用して行うことができます。このメソッドを使用してセッションに保存されたデータは、後続の HTTP リクエスト中にすぐに使用できるようになります。後続の HTTP リクエストの後、フラッシュされたデータは削除されます。フラッシュ データは主に、短期間のステータス メッセージに役立ちます。

    $request->session()->flash('status', 'Task was successful!');

複数のリクエストに対してフラッシュ データを保持する必要がある場合は、追加のリクエストに備えてすべてのフラッシュ データを保持する `reflash` メソッドを使用できます。特定のフラッシュ データのみを保持する必要がある場合は、`keep` メソッドを使用できます。

    $request->session()->reflash();

    $request->session()->keep(['username', 'email']);

現在のリクエストに対してのみフラッシュ データを保持するには、`now` メソッドを使用できます。

    $request->session()->now('status', 'Task was successful!');

<a name="deleting-data"></a>
### データの削除

`forget` メソッドは、セッションからデータの一部を削除します。セッションからすべてのデータを削除したい場合は、`flush` メソッドを使用できます。

    // Forget a single key...
    $request->session()->forget('name');

    // Forget multiple keys...
    $request->session()->forget(['name', 'status']);

    $request->session()->flush();

<a name="regenerating-the-session-id"></a>
### セッションIDの再生成

セッション ID の再生成は、悪意のあるユーザーがアプリケーションに対して [セッション固定](https://owasp.org/www-community/attacks/Session_fixation) 攻撃を悪用するのを防ぐために行われることがよくあります。

Laravel [アプリケーションスターターキット](/docs/{{version}}/starter-kits) または [Laravel の強化](/docs/{{version}}/fortify) のいずれかを使用している場合、Laravel は認証中にセッション ID を自動的に再生成します。ただし、セッション ID を手動で再生成する必要がある場合は、`regenerate` メソッドを使用できます。

    $request->session()->regenerate();

単一のステートメントでセッション ID を再生成し、セッションからすべてのデータを削除する必要がある場合は、`invalidate` メソッドを使用できます。

    $request->session()->invalidate();

<a name="session-blocking"></a>
## セッションのブロック (Session Blocking)

> **警告**
> セッション ブロッキングを利用するには、アプリケーションで [アトミックロック](/docs/{{version}}/cache#atomic-locks) をサポートするキャッシュ ドライバを使用する必要があります。現在、これらのキャッシュ ドライバには、`memcached`、`dynamodb`、`redis`、および `database` ドライバが含まれます。また、`cookie` セッション ドライバは使用できません。

デフォルトでは、Laravel は同じセッションを使用したリクエストの同時実行を許可します。したがって、たとえば、JavaScript HTTP ライブラリを使用してアプリケーションに対して 2 つの HTTP リクエストを作成すると、両方が同時に実行されます。多くのアプリケーションでは、これは問題になりません。ただし、セッション データの損失は、両方ともセッションにデータを書き込む 2 つの異なるアプリケーション エンドポイントに同時にリクエストを行うアプリケーションの小さなサブセットで発生する可能性があります。

これを軽減するために、Laravel は特定のセッションの同時リクエストを制限できる機能を提供します。まず、`block` メソッドをルート定義にチェーンするだけです。この例では、`/profile` エンドポイントへの受信リクエストはセッション ロックを取得します。このロックが保持されている間、同じセッション ID を共有する `/profile` または `/order` エンドポイントへの受信リクエストは、最初のリクエストの実行が完了するまで待機してから、実行を続行します。

    Route::post('/profile', function () {
        //
    })->block($lockSeconds = 10, $waitSeconds = 10)

    Route::post('/order', function () {
        //
    })->block($lockSeconds = 10, $waitSeconds = 10)

`block` メソッドは 2 つのオプションの引数を受け入れます。 `block` メソッドで受け入れられる最初の引数は、セッション ロックが解放されるまで保持される最大秒数です。もちろん、この時間より前にリクエストの実行が終了した場合、ロックはより早く解放されます。

`block` メソッドで受け入れられる 2 番目の引数は、セッション ロックの取得を試行する際にリクエストが待機する秒数です。リクエストが指定された秒数以内にセッション ロックを取得できない場合、`Illuminate\Contracts\Cache\LockTimeoutException` がスローされます。

これらの引数のどちらも渡されない場合、ロックは最大 10 秒間取得され、リクエストはロックの取得を試行する間最大 10 秒待機します。

    Route::post('/profile', function () {
        //
    })->block()

<a name="adding-custom-session-drivers"></a>
## カスタムセッションドライバの追加 (Adding Custom Session Drivers)

<a name="implementing-the-driver"></a>
#### ドライバの実装

既存のセッションドライバがアプリケーションのニーズに適合しない場合は、Laravel を使用して独自のセッションハンドラーを作成できます。カスタム セッション ドライバは、PHP の組み込み `SessionHandlerInterface` を実装する必要があります。このインターフェイスには、いくつかの簡単なメソッドが含まれています。スタブ化された MongoDB 実装は次のようになります。

    <?php

    namespace App\Extensions;

    class MongoSessionHandler implements \SessionHandlerInterface
    {
        public function open($savePath, $sessionName) {}
        public function close() {}
        public function read($sessionId) {}
        public function write($sessionId, $data) {}
        public function destroy($sessionId) {}
        public function gc($lifetime) {}
    }

> **注記**
> Laravel には、拡張機能を含めるディレクトリは付属していません。好きな場所に自由に配置できます。この例では、`MongoSessionHandler` を格納する `Extensions` ディレクトリを作成しました。

これらのメソッドの目的はすぐには理解できないため、各メソッドの機能を簡単に説明します。

<div class="content-list" markdown="1">

- `open` メソッドは通常、ファイル ベースのセッション ストア システムで使用されます。 Laravel には `file` セッションドライバが同梱されているため、このメソッドに何も入れる必要はほとんどありません。このメソッドは空のままにすることができます。
- `close` メソッドも、`open` メソッドと同様に、通常は無視できます。ほとんどのドライバでは必要ありません。
- `read` メソッドは、指定された `$sessionId` に関連付けられたセッション データの文字列バージョンを返す必要があります。 Laravel がシリアル化を実行するため、ドライバでセッション データを取得または保存するときにシリアル化やその他のエンコードを行う必要はありません。
- `write` メソッドは、`$sessionId` に関連付けられた特定の `$data` 文字列を、MongoDB や選択した別のストレージ システムなどの永続ストレージ システムに書き込む必要があります。  繰り返しますが、シリアル化を実行しないでください。Laravel がすでにシリアル化を処理します。
- `destroy` メソッドは、`$sessionId` に関連付けられたデータを永続ストレージから削除する必要があります。
- `gc` メソッドは、指定された `$lifetime` (UNIX タイムスタンプ) より古いセッション データをすべて破棄する必要があります。 Memcached や Redis などの自己期限切れシステムの場合、このメソッドは空のままにすることができます。

</div>

<a name="registering-the-driver"></a>
#### ドライバを登録する

ドライバが実装されたら、Laravel に登録する準備が整います。 Laravel のセッション バックエンドに追加のドライバを追加するには、`Session` [facade](/docs/{{version}}/facades) によって提供される `extend` メソッドを使用できます。 [サービスプロバイダ](/docs/{{version}}/providers) の `boot` メソッドから `extend` メソッドを呼び出す必要があります。既存の `App\Providers\AppServiceProvider` からこれを行うことも、まったく新しいプロバイダを作成することもできます。

    <?php

    namespace App\Providers;

    use App\Extensions\MongoSessionHandler;
    use Illuminate\Support\Facades\Session;
    use Illuminate\Support\ServiceProvider;

    class SessionServiceProvider extends ServiceProvider
    {
        /**
         * Register any application services.
         *
         * @return void
         */
        public function register()
        {
            //
        }

        /**
         * Bootstrap any application services.
         *
         * @return void
         */
        public function boot()
        {
            Session::extend('mongo', function ($app) {
                // Return an implementation of SessionHandlerInterface...
                return new MongoSessionHandler;
            });
        }
    }

セッションドライバが登録されると、`config/session.php` 構成ファイルで `mongo` ドライバを使用できるようになります。

