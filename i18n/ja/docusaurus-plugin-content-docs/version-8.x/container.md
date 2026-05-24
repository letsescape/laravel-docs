# サービスコンテナ (Service Container)

- [Introduction](#introduction)
    - [ゼロ構成の解決策](#zero-configuration-resolution)
    - [コンテナを使用する場合](#when-to-use-the-container)
- [Binding](#binding)
    - [バインディングの基本](#binding-basics)
    - [インターフェースを実装にバインドする](#binding-interfaces-to-implementations)
    - [コンテキストバインディング](#contextual-binding)
    - [バインディングプリミティブ](#binding-primitives)
    - [型付き可変個引数のバインディング](#binding-typed-variadics)
    - [Tagging](#tagging)
    - [バインディングの拡張](#extending-bindings)
- [Resolving](#resolving)
    - [Make メソッド](#the-make-method)
    - [自動注入](#automatic-injection)
- [メソッドの呼び出しと注入](#method-invocation-and-injection)
- [コンテナイベント](#container-events)
- [PSR-11](#psr-11)

<a name="introduction"></a>
## 導入 (Introduction)

Laravel サービスコンテナは、クラスの依存関係を管理し、依存関係の注入を実行するための強力なツールです。依存関係の注入とは、本質的には次のことを意味する派手な表現です。クラスの依存関係は、コンストラクター、または場合によっては「セッター」メソッドを介してクラスに「注入」されます。

簡単な例を見てみましょう。

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use App\Repositories\UserRepository;
    use App\Models\User;

    class UserController extends Controller
    {
        /**
         * The user repository implementation.
         *
         * @var UserRepository
         */
        protected $users;

        /**
         * Create a new controller instance.
         *
         * @param  UserRepository  $users
         * @return void
         */
        public function __construct(UserRepository $users)
        {
            $this->users = $users;
        }

        /**
         * Show the profile for the given user.
         *
         * @param  int  $id
         * @return Response
         */
        public function show($id)
        {
            $user = $this->users->find($id);

            return view('user.profile', ['user' => $user]);
        }
    }

この例では、`UserController` はデータ ソースからユーザーを取得する必要があります。そこで、ユーザーを取得できるサービスを**挿入**します。このコンテキストでは、`UserRepository` はおそらく [Eloquent](/docs/{{version}}/eloquent) を使用してデータベースからユーザー情報を取得します。ただし、リポジトリは挿入されるため、別の実装と簡単に交換できます。また、アプリケーションをテストするときに、簡単に「モック」したり、`UserRepository` のダミー実装を作成したりすることもできます。

Laravel サービスコンテナを深く理解することは、強力で大規模なアプリケーションを構築するだけでなく、Laravel コア自体に貢献するためにも不可欠です。

<a name="zero-configuration-resolution"></a>
### ゼロ構成の解決策

クラスに依存関係がない場合、または他の具象クラス (インターフェイスではない) にのみ依存する場合、コンテナーにそのクラスを解決する方法を指示する必要はありません。たとえば、次のコードを `routes/web.php` ファイルに配置できます。

    <?php

    class Service
    {
        //
    }

    Route::get('/', function (Service $service) {
        die(get_class($service));
    });

この例では、アプリケーションの `/` ルートにアクセスすると、自動的に `Service` クラスが解決され、それがルートのハンドラーに挿入されます。これはゲームチェンジです。つまり、肥大化した構成ファイルを気にせずにアプリケーションを開発し、依存関係の注入を活用できるということです。

ありがたいことに、Laravel アプリケーションを構築するときに作成するクラスの多くは、[controllers](/docs/{{version}}/controllers)、[イベントリスナ](/docs/{{version}}/events)、[middleware](/docs/{{version}}/middleware) などの依存関係をコンテナ経由で自動的に受け取ります。さらに、[キューに入れられたジョブ](/docs/{{version}}/queues) の `handle` メソッドで依存関係をタイプヒントすることもできます。自動かつ構成ゼロの依存注入の威力を一度味わってしまうと、それなしで開発することは不可能に感じられます。

<a name="when-to-use-the-container"></a>
### コンテナを使用する場合

構成解決が不要なため、コンテナーと手動でやり取りすることなく、ルート、コントローラ、イベント リスナなどの依存関係をタイプヒントで確認できるようになります。たとえば、現在のリクエストに簡単にアクセスできるように、ルート定義で `Illuminate\Http\Request` オブジェクトにタイプヒントを指定できます。このコードを記述するためにコンテナーと対話する必要はありませんが、コンテナーはバックグラウンドでこれらの依存関係の注入を管理しています。

    use Illuminate\Http\Request;

    Route::get('/', function (Request $request) {
        // ...
    });

多くの場合、自動依存注入と [facades](/docs/{{version}}/facades) のおかげで、コンテナから何も手動でバインドしたり解決したりすることなく、Laravel アプリケーションを構築できます。 **それでは、コンテナを手動で操作するのはどのような場合でしょうか?** 2 つの状況を調べてみましょう。

まず、インターフェイスを実装するクラスを作成し、ルートまたはクラス コンストラクターでそのインターフェイスをタイプヒントで指定したい場合は、[そのインターフェイスを解決する方法をコンテナに指示します](#binding-interfaces-to-implementations) を実行する必要があります。次に、他の Laravel 開発者と共有する予定の [Laravelパッケージを書く](/docs/{{version}}/packages) の場合は、パッケージのサービスをコンテナにバインドする必要がある場合があります。

<a name="binding"></a>
## バインディング (Binding)

<a name="binding-basics"></a>
### バインディングの基本

<a name="simple-bindings"></a>
#### シンプルなバインディング

ほとんどすべてのサービスコンテナー バインディングは [サービスプロバイダ](/docs/{{version}}/providers) 内に登録されるため、これらの例のほとんどは、そのコンテキストでコンテナーを使用する方法を示しています。

サービスプロバイダ内では、`$this->app` プロパティを介して常にコンテナーにアクセスできます。 `bind` メソッドを使用してバインディングを登録し、クラスのインスタンスを返すクロージャとともに登録したいクラス名またはインターフェイス名を渡します。

    use App\Services\Transistor;
    use App\Services\PodcastParser;

    $this->app->bind(Transistor::class, function ($app) {
        return new Transistor($app->make(PodcastParser::class));
    });

コンテナ自体をリゾルバーへの引数として受け取ることに注意してください。その後、コンテナを使用して、構築しているオブジェクトのサブ依存関係を解決できます。

前述したように、通常はサービスプロバイダ内のコンテナーと対話します。ただし、サービスプロバイダの外部でコンテナーと対話したい場合は、`App` [facade](/docs/{{version}}/facades) 経由で行うことができます。

    use App\Services\Transistor;
    use Illuminate\Support\Facades\App;

    App::bind(Transistor::class, function ($app) {
        // ...
    });

> {tip} クラスがインターフェイスに依存しない場合、クラスをコンテナにバインドする必要はありません。コンテナはリフレクションを使用してこれらのオブジェクトを自動的に解決できるため、これらのオブジェクトの構築方法を指示する必要はありません。

<a name="binding-a-singleton"></a>
#### シングルトンのバインド

`singleton` メソッドは、クラスまたはインターフェイスをコンテナーにバインドしますが、解決されるのは 1 回だけです。シングルトン バインディングが解決されると、コンテナへの後続の呼び出しで同じオブジェクト インスタンスが返されます。

    use App\Services\Transistor;
    use App\Services\PodcastParser;

    $this->app->singleton(Transistor::class, function ($app) {
        return new Transistor($app->make(PodcastParser::class));
    });

<a name="binding-scoped"></a>
#### スコープ指定されたシングルトンのバインディング

`scoped` メソッドは、特定の Laravel リクエスト/ジョブのライフサイクル内で 1 回だけ解決されるクラスまたはインターフェイスをコンテナーにバインドします。このメソッドは `singleton` メソッドに似ていますが、`scoped` メソッドを使用して登録されたインスタンスは、[Laravel Octane](/docs/{{version}}/octane) ワーカーが新しいリクエストを処理するときや、Laravel [キューワーカー](/docs/{{version}}/queues) が新しいジョブを処理するときなど、Laravel アプリケーションが新しい「ライフサイクル」を開始するたびにフラッシュされます。

    use App\Services\Transistor;
    use App\Services\PodcastParser;

    $this->app->scoped(Transistor::class, function ($app) {
        return new Transistor($app->make(PodcastParser::class));
    });

<a name="binding-instances"></a>
#### バインディングインスタンス

`instance` メソッドを使用して、既存のオブジェクト インスタンスをコンテナにバインドすることもできます。指定されたインスタンスは、コンテナへの後続の呼び出しで常に返されます。

    use App\Services\Transistor;
    use App\Services\PodcastParser;

    $service = new Transistor(new PodcastParser);

    $this->app->instance(Transistor::class, $service);

<a name="binding-interfaces-to-implementations"></a>
### インターフェースを実装にバインドする

サービスコンテナの非常に強力な機能は、インターフェイスを特定の実装にバインドできることです。たとえば、`EventPusher` インターフェイスと `RedisEventPusher` 実装があると仮定します。このインターフェースの `RedisEventPusher` 実装をコーディングしたら、次のようにサービスコンテナーに登録できます。

    use App\Contracts\EventPusher;
    use App\Services\RedisEventPusher;

    $this->app->bind(EventPusher::class, RedisEventPusher::class);

このステートメントは、クラスが `EventPusher` の実装を必要とする場合に、`RedisEventPusher` を注入する必要があることをコンテナーに指示します。これで、コンテナーによって解決されるクラスのコンストラクターで `EventPusher` インターフェイスをタイプヒントできるようになりました。 Laravel アプリケーション内のコントローラ、イベントリスナ、ミドルウェア、その他のさまざまなタイプのクラスは、常にコンテナーを使用して解決されることに注意してください。

    use App\Contracts\EventPusher;

    /**
     * Create a new class instance.
     *
     * @param  \App\Contracts\EventPusher  $pusher
     * @return void
     */
    public function __construct(EventPusher $pusher)
    {
        $this->pusher = $pusher;
    }

<a name="contextual-binding"></a>
### コンテキストバインディング

同じインターフェイスを利用する 2 つのクラスがあり、各クラスに異なる実装を挿入したい場合があります。たとえば、2 つのコントローラが `Illuminate\Contracts\Filesystem\Filesystem` [contract](/docs/{{version}}/contracts) の異なる実装に依存している場合があります。 Laravel は、この動作を定義するためのシンプルで流暢なインターフェイスを提供します。

    use App\Http\Controllers\PhotoController;
    use App\Http\Controllers\UploadController;
    use App\Http\Controllers\VideoController;
    use Illuminate\Contracts\Filesystem\Filesystem;
    use Illuminate\Support\Facades\Storage;

    $this->app->when(PhotoController::class)
              ->needs(Filesystem::class)
              ->give(function () {
                  return Storage::disk('local');
              });

    $this->app->when([VideoController::class, UploadController::class])
              ->needs(Filesystem::class)
              ->give(function () {
                  return Storage::disk('s3');
              });

<a name="binding-primitives"></a>
### バインディングプリミティブ

場合によっては、注入されたクラスを受け取るクラスが、整数などの注入されたプリミティブ値も必要とする場合があります。コンテキスト バインディングを使用して、クラスに必要な値を簡単に注入できます。

    $this->app->when('App\Http\Controllers\UserController')
              ->needs('$variableName')
              ->give($value);

クラスが [tagged](#tagging) インスタンスの配列に依存する場合があります。 `giveTagged` メソッドを使用すると、そのタグを含むすべてのコンテナー バインディングを簡単に挿入できます。

    $this->app->when(ReportAggregator::class)
        ->needs('$reports')
        ->giveTagged('reports');

アプリケーションの構成ファイルの 1 つから値を挿入する必要がある場合は、`giveConfig` メソッドを使用できます。

    $this->app->when(ReportAggregator::class)
        ->needs('$timezone')
        ->giveConfig('app.timezone');

<a name="binding-typed-variadics"></a>
### 型付き可変個引数のバインディング

場合によっては、可変長コンストラクター引数を使用して型指定されたオブジェクトの配列を受け取るクラスがある場合があります。

    <?php

    use App\Models\Filter;
    use App\Services\Logger;

    class Firewall
    {
        /**
         * The logger instance.
         *
         * @var \App\Services\Logger
         */
        protected $logger;

        /**
         * The filter instances.
         *
         * @var array
         */
        protected $filters;

        /**
         * Create a new class instance.
         *
         * @param  \App\Services\Logger  $logger
         * @param  array  $filters
         * @return void
         */
        public function __construct(Logger $logger, Filter ...$filters)
        {
            $this->logger = $logger;
            $this->filters = $filters;
        }
    }

コンテキスト バインディングを使用すると、解決された `Filter` インスタンスの配列を返すクロージャを `give` メソッドに提供することで、この依存関係を解決できます。

    $this->app->when(Firewall::class)
              ->needs(Filter::class)
              ->give(function ($app) {
                    return [
                        $app->make(NullFilter::class),
                        $app->make(ProfanityFilter::class),
                        $app->make(TooLongFilter::class),
                    ];
              });

便宜上、`Firewall` が `Filter` インスタンスを必要とするときに、コンテナーによって解決されるクラス名の配列を指定することもできます。

    $this->app->when(Firewall::class)
              ->needs(Filter::class)
              ->give([
                  NullFilter::class,
                  ProfanityFilter::class,
                  TooLongFilter::class,
              ]);

<a name="variadic-tag-dependencies"></a>
#### 可変引数タグの依存関係

場合によっては、クラスに、特定のクラス (`Report ...$reports`) としてタイプヒントされる可変個引数の依存関係がある場合があります。 `needs` メソッドと `giveTagged` メソッドを使用すると、指定された依存関係の [tag](#tagging) を持つすべてのコンテナー バインディングを簡単に注入できます。

    $this->app->when(ReportAggregator::class)
        ->needs(Report::class)
        ->giveTagged('reports');

<a name="tagging"></a>
### タグ付け

場合によっては、バインディングの特定の「カテゴリ」をすべて解決する必要がある場合があります。たとえば、さまざまな `Report` インターフェイス実装の配列を受け取るレポート アナライザーを構築しているとします。 `Report` 実装を登録した後、`tag` メソッドを使用してタグを割り当てることができます。

    $this->app->bind(CpuReport::class, function () {
        //
    });

    $this->app->bind(MemoryReport::class, function () {
        //
    });

    $this->app->tag([CpuReport::class, MemoryReport::class], 'reports');

サービスにタグを付けたら、コンテナーの `tagged` メソッドを使用してすべてを簡単に解決できます。

    $this->app->bind(ReportAnalyzer::class, function ($app) {
        return new ReportAnalyzer($app->tagged('reports'));
    });

<a name="extending-bindings"></a>
### バインディングの拡張

`extend` メソッドを使用すると、解決されたサービスを変更できます。たとえば、サービスが解決されると、追加のコードを実行してサービスを修飾または構成することができます。 `extend` メソッドは、変更されたサービスを返すクロージャを唯一の引数として受け入れます。クロージャーは、解決されるサービスとコンテナー インスタンスを受け取ります。

    $this->app->extend(Service::class, function ($service, $app) {
        return new DecoratedService($service);
    });

<a name="resolving"></a>
## 解決する (Resolving)

<a name="the-make-method"></a>
### `make` メソッド

`make` メソッドを使用して、コンテナからクラス インスタンスを解決できます。 `make` メソッドは、解決するクラスまたはインターフェイスの名前を受け入れます。

    use App\Services\Transistor;

    $transistor = $this->app->make(Transistor::class);

クラスの依存関係の一部がコンテナー経由で解決できない場合は、それらを連想配列として `makeWith` メソッドに渡すことによって注入できます。たとえば、`Transistor` サービスに必要な `$id` コンストラクター引数を手動で渡すことができます。

    use App\Services\Transistor;

    $transistor = $this->app->makeWith(Transistor::class, ['id' => 1]);

サービスプロバイダの外部で、`$app` 変数にアクセスできないコードの場所にいる場合は、`App` [facade](/docs/{{version}}/facades) を使用して、コンテナーからクラス インスタンスを解決できます。

    use App\Services\Transistor;
    use Illuminate\Support\Facades\App;

    $transistor = App::make(Transistor::class);

Laravelコンテナインスタンス自体を、コンテナによって解決されるクラスに挿入したい場合は、クラスのコンストラクタで`Illuminate\Container\Container`クラスをタイプヒントできます。

    use Illuminate\Container\Container;

    /**
     * Create a new class instance.
     *
     * @param  \Illuminate\Container\Container  $container
     * @return void
     */
    public function __construct(Container $container)
    {
        $this->container = $container;
    }

<a name="automatic-injection"></a>
### 自動注入

あるいは、重要なことですが、[controllers](/docs/{{version}}/controllers)、[イベントリスナ](/docs/{{version}}/events)、[middleware](/docs/{{version}}/middleware) など、コンテナーによって解決されるクラスのコンストラクター内の依存関係をタイプヒントで指定することもできます。さらに、[キューに入れられたジョブ](/docs/{{version}}/queues) の `handle` メソッドで依存関係をタイプヒントすることもできます。実際には、これがほとんどのオブジェクトがコンテナによって解決される方法です。

たとえば、コントローラのコンストラクターでアプリケーションによって定義されたリポジトリをタイプヒントで指定できます。リポジトリは自動的に解決され、クラスに挿入されます。

    <?php

    namespace App\Http\Controllers;

    use App\Repositories\UserRepository;

    class UserController extends Controller
    {
        /**
         * The user repository instance.
         *
         * @var \App\Repositories\UserRepository
         */
        protected $users;

        /**
         * Create a new controller instance.
         *
         * @param  \App\Repositories\UserRepository  $users
         * @return void
         */
        public function __construct(UserRepository $users)
        {
            $this->users = $users;
        }

        /**
         * Show the user with the given ID.
         *
         * @param  int  $id
         * @return \Illuminate\Http\Response
         */
        public function show($id)
        {
            //
        }
    }

<a name="method-invocation-and-injection"></a>
## メソッドの呼び出しと注入 (Method Invocation & Injection)

場合によっては、コンテナーがそのメソッドの依存関係を自動的に挿入できるようにしながら、オブジェクト インスタンスでメソッドを呼び出したい場合があります。たとえば、次のクラスがあるとします。

    <?php

    namespace App;

    use App\Repositories\UserRepository;

    class UserReport
    {
        /**
         * Generate a new user report.
         *
         * @param  \App\Repositories\UserRepository  $repository
         * @return array
         */
        public function generate(UserRepository $repository)
        {
            // ...
        }
    }

次のようにコンテナ経由で `generate` メソッドを呼び出すことができます。

    use App\UserReport;
    use Illuminate\Support\Facades\App;

    $report = App::call([new UserReport, 'generate']);

`call` メソッドは、任意の PHP 呼び出し可能メソッドを受け入れます。コンテナーの `call` メソッドを使用して、依存関係を自動的に注入しながらクロージャーを呼び出すこともできます。

    use App\Repositories\UserRepository;
    use Illuminate\Support\Facades\App;

    $result = App::call(function (UserRepository $repository) {
        // ...
    });

<a name="container-events"></a>
## コンテナイベント (Container Events)

サービスコンテナは、オブジェクトを解決するたびにイベントを起動します。 `resolving` メソッドを使用して、このイベントをリッスンできます。

    use App\Services\Transistor;

    $this->app->resolving(Transistor::class, function ($transistor, $app) {
        // Called when container resolves objects of type "Transistor"...
    });

    $this->app->resolving(function ($object, $app) {
        // Called when container resolves object of any type...
    });

ご覧のとおり、解決されるオブジェクトはコールバックに渡されるため、コンシューマーに渡される前にオブジェクトに追加のプロパティを設定できるようになります。

<a name="psr-11"></a>
## PSR-11 (PSR-11)

Laravelのサービスコンテナは[PSR-11](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-11-container.md)インターフェースを実装しています。したがって、PSR-11 コンテナ インターフェイスにタイプヒントを入力して、Laravel コンテナのインスタンスを取得できます。

    use App\Services\Transistor;
    use Psr\Container\ContainerInterface;

    Route::get('/', function (ContainerInterface $container) {
        $service = $container->get(Transistor::class);

        //
    });

指定された識別子を解決できない場合は、例外がスローされます。識別子がバインドされていない場合、例外は `Psr\Container\NotFoundExceptionInterface` のインスタンスになります。識別子がバインドされているが解決できなかった場合、`Psr\Container\ContainerExceptionInterface` のインスタンスがスローされます。

