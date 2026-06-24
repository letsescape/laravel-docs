<!-- # Request Lifecycle -->
# Request Lifecycle

- [Introduction](#introduction)
- [Lifecycle Overview](#lifecycle-overview)
    - [First Steps](#first-steps)
    - [HTTP / Console Kernels](#http-console-kernels)
    - [Service Providers](#service-providers)
    - [Routing](#routing)
    - [Finishing Up](#finishing-up)
- [Focus on Service Providers](#focus-on-service-providers)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- When using any tool in the "real world", you feel more confident if you understand how that tool works. Application development is no different. When you understand how your development tools function, you feel more comfortable and confident using them. -->
「現実世界」でツールを使用するとき、そのツールがどのように機能するかを理解していれば、より自信が持てるようになります。アプリケーション開発も同様です。開発ツールがどのように機能するかを理解すると、より快適に、自信を持って開発ツールを使用できるようになります。

<!-- The goal of this document is to give you a good, high-level overview of how the Laravel framework works. By getting to know the overall framework better, everything feels less "magical" and you will be more confident building your applications. If you don't understand all of the terms right away, don't lose heart! Just try to get a basic grasp of what is going on, and your knowledge will grow as you explore other sections of the documentation. -->
このドキュメントの目的は、Laravel フレームワークがどのように機能するかについての概要をわかりやすく説明することです。全体的なフレームワークをより深く理解することで、すべてが「魔法」のように感じられなくなり、より自信を持ってアプリケーションを構築できるようになります。用語のすべてをすぐに理解できなくても、がっかりしないでください。何が起こっているのかを基本的に理解するように努めてください。ドキュメントの他のセクションを調べるにつれて知識が深まります。

<a name="lifecycle-overview"></a>
<!-- ## Lifecycle Overview -->
## Lifecycle Overview

<a name="first-steps"></a>
<!-- ### First Steps -->
### First Steps

<!-- The entry point for all requests to a Laravel application is the `public/index.php` file. All requests are directed to this file by your web server (Apache / Nginx) configuration. The `index.php` file doesn't contain much code. Rather, it is a starting point for loading the rest of the framework. -->
Laravel アプリケーションへのすべてのリクエストのエントリ ポイントは、`public/index.php` ファイルです。すべてのリクエストは、Web サーバー (Apache / Nginx) 構成によってこのファイルに送信されます。 `index.php` ファイルには多くのコードは含まれていません。むしろ、これはフレームワークの残りの部分をロードするための開始点です。

<!-- The `index.php` file loads the Composer generated autoloader definition, and then retrieves an instance of the Laravel application from `bootstrap/app.php`. The first action taken by Laravel itself is to create an instance of the application / [service container](/docs/11.x/container). -->
`index.php` ファイルは、Composer で生成されたオートローダー定義をロードし、`bootstrap/app.php` から Laravel アプリケーションのインスタンスを取得します。 Laravel 自体によって実行される最初のアクションは、アプリケーション / [service container](/docs/11.x/container) のインスタンスを作成することです。

<a name="http-console-kernels"></a>
<!-- ### HTTP / Console Kernels -->
### HTTP / Console Kernels

<!-- Next, the incoming request is sent to either the HTTP kernel or the console kernel, using the `handleRequest` or `handleCommand` methods of the application instance, depending on the type of request entering the application. These two kernels serve as the central location through which all requests flow. For now, let's just focus on the HTTP kernel, which is an instance of `Illuminate\Foundation\Http\Kernel`. -->
次に、アプリケーションに入るリクエストのタイプに応じて、アプリケーション インスタンスの `handleRequest` メソッドまたは `handleCommand` メソッドを使用して、受信リクエストが HTTP カーネルまたはコンソール カーネルのいずれかに送信されます。これら 2 つのカーネルは、すべてのリクエストが流れる中心的な場所として機能します。ここでは、`Illuminate\Foundation\Http\Kernel` のインスタンスである HTTP カーネルに注目してみましょう。

<!-- The HTTP kernel defines an array of `bootstrappers` that will be run before the request is executed. These bootstrappers configure error handling, configure logging, [detect the application environment](/docs/11.x/configuration#environment-configuration), and perform other tasks that need to be done before the request is actually handled. Typically, these classes handle internal Laravel configuration that you do not need to worry about. -->
HTTP カーネルは、リクエストが実行される前に実行される `bootstrappers` の配列を定義します。これらのブートストラップは、エラー処理の構成、ロギング、[detect the application environment](/docs/11.x/configuration#environment-configuration) の構成、およびリクエストが実際に処理される前に実行する必要があるその他のタスクを実行します。通常、これらのクラスは、心配する必要のない内部 Laravel 設定を処理します。

<!-- The HTTP kernel is also responsible for passing the request through the application's middleware stack. These middleware handle reading and writing the [HTTP session](/docs/11.x/session), determining if the application is in maintenance mode, [verifying the CSRF token](/docs/11.x/csrf), and more. We'll talk more about these soon. -->
HTTP カーネルは、アプリケーションのミドルウェア スタックを通じてリクエストを渡す役割も担います。これらのミドルウェアは、[HTTP session](/docs/11.x/session) の読み取りと書き込みを処理し、アプリケーションがメンテナンス モードであるかどうかや [verifying the CSRF token](/docs/11.x/csrf) などを判断します。これらについては、後ほど詳しく説明します。

<!-- The method signature for the HTTP kernel's `handle` method is quite simple: it receives a `Request` and returns a `Response`. Think of the kernel as being a big black box that represents your entire application. Feed it HTTP requests and it will return HTTP responses. -->
HTTP カーネルの `handle` メソッドのメソッド シグネチャは非常に単純です。`Request` を受け取り、`Response` を返します。カーネルは、アプリケーション全体を表す大きなブラック ボックスであると考えてください。 HTTP リクエストを入力すると、HTTP レスポンスが返されます。

<a name="service-providers"></a>
<!-- ### Service Providers -->
### Service Providers

<!-- One of the most important kernel bootstrapping actions is loading the [service providers](/docs/11.x/providers) for your application. Service providers are responsible for bootstrapping all of the framework's various components, such as the database, queue, validation, and routing components. -->
最も重要なカーネル ブートストラップ アクションの 1 つは、アプリケーションの [service providers](/docs/11.x/providers) をロードすることです。サービスプロバイダは、データベース、キュー、検証、ルーティング コンポーネントなど、フレームワークのさまざまなコンポーネントをすべてブートストラップする責任があります。

<!-- Laravel will iterate through this list of providers and instantiate each of them. After instantiating the providers, the `register` method will be called on all of the providers. Then, once all of the providers have been registered, the `boot` method will be called on each provider. This is so service providers may depend on every container binding being registered and available by the time their `boot` method is executed. -->
Laravel は、このプロバイダのリストを反復処理し、それぞれをインスタンス化します。プロバイダをインスタンス化した後、すべてのプロバイダで `register` メソッドが呼び出されます。次に、すべてのプロバイダが登録されると、`boot` メソッドが各プロバイダで呼び出されます。これは、サービスプロバイダが、`boot` メソッドが実行されるまでに登録され、利用可能になっているすべてのコンテナー バインディングに依存できるようにするためです。

<!-- Essentially every major feature offered by Laravel is bootstrapped and configured by a service provider. Since they bootstrap and configure so many features offered by the framework, service providers are the most important aspect of the entire Laravel bootstrap process. -->
基本的に、Laravel が提供するすべての主要な機能は、サービスプロバイダによってブートストラップされ、設定されます。サービスプロバイダは、フレームワークによって提供される非常に多くの機能をブートストラップして構成するため、Laravel ブートストラッププロセス全体の最も重要な側面となります。

<!-- While the framework internally uses dozens of service providers, you also have the option to create your own. You can find a list of the user-defined or third-party service providers that your application is using in the `bootstrap/providers.php` file. -->
フレームワークは内部で多数のサービスプロバイダを使用しますが、独自のサービスプロバイダを作成するオプションもあります。アプリケーションが使用しているユーザー定義またはサードパーティのサービスプロバイダのリストは、`bootstrap/providers.php` ファイルで確認できます。

<a name="routing"></a>
<!-- ### Routing -->
### Routing

<!-- Once the application has been bootstrapped and all service providers have been registered, the `Request` will be handed off to the router for dispatching. The router will dispatch the request to a route or controller, as well as run any route specific middleware. -->
アプリケーションがブートストラップされ、すべてのサービスプロバイダが登録されると、`Request` がディスパッチのためにルーターに渡されます。ルーターはリクエストをルートまたはコントローラにディスパッチし、ルート固有のミドルウェアを実行します。

<!-- Middleware provide a convenient mechanism for filtering or examining HTTP requests entering your application. For example, Laravel includes a middleware that verifies if the user of your application is authenticated. If the user is not authenticated, the middleware will redirect the user to the login screen. However, if the user is authenticated, the middleware will allow the request to proceed further into the application. Some middleware are assigned to all routes within the application, like `PreventRequestsDuringMaintenance`, while some are only assigned to specific routes or route groups. You can learn more about middleware by reading the complete [middleware documentation](/docs/11.x/middleware). -->
ミドルウェアは、アプリケーションに入る HTTP リクエストをフィルタリングまたは検査するための便利なメカニズムを提供します。たとえば、Laravel には、アプリケーションのユーザーが認証されているかどうかを検証するミドルウェアが含まれています。ユーザーが認証されていない場合、ミドルウェアはユーザーをログイン画面にリダイレクトします。ただし、ユーザーが認証されている場合、ミドルウェアはリクエストがアプリケーション内にさらに進むことを許可します。 `PreventRequestsDuringMaintenance` のように、アプリケーション内のすべてのルートに割り当てられるミドルウェアもあれば、特定のルートまたはルート グループにのみ割り当てられるミドルウェアもあります。 [middleware documentation](/docs/11.x/middleware) を完全に読むことで、ミドルウェアの詳細を学ぶことができます。

<!-- If the request passes through all of the matched route's assigned middleware, the route or controller method will be executed and the response returned by the route or controller method will be sent back through the route's chain of middleware. -->
リクエストが、一致したルートに割り当てられたすべてのミドルウェアを通過する場合、ルートまたはコントローラ メソッドが実行され、ルートまたはコントローラ メソッドによって返された応答は、ルートのミドルウェア チェーンを通じて送り返されます。

<a name="finishing-up"></a>
<!-- ### Finishing Up -->
### Finishing Up

<!-- Once the route or controller method returns a response, the response will travel back outward through the route's middleware, giving the application a chance to modify or examine the outgoing response. -->
ルートまたはコントローラ メソッドが応答を返すと、その応答はルートのミドルウェアを介して外向きに戻り、アプリケーションに送信される応答を変更または検査する機会が与えられます。

<!-- Finally, once the response travels back through the middleware, the HTTP kernel's `handle` method returns the response object to the `handleRequest` of the application instance, and this method calls the `send` method on the returned response. The `send` method sends the response content to the user's web browser. We've now completed our journey through the entire Laravel request lifecycle! -->
最後に、応答がミドルウェアを介して戻ってくると、HTTP カーネルの `handle` メソッドは応答オブジェクトをアプリケーション インスタンスの `handleRequest` に返し、このメソッドは返された応答に対して `send` メソッドを呼び出します。 `send` メソッドは、応答コンテンツをユーザーの Web ブラウザーに送信します。これで、Laravel リクエストのライフサイクル全体にわたる旅が完了しました。

<a name="focus-on-service-providers"></a>
<!-- ## Focus on Service Providers -->
## Focus on Service Providers

<!-- Service providers are truly the key to bootstrapping a Laravel application. The application instance is created, the service providers are registered, and the request is handed to the bootstrapped application. It's really that simple! -->
サービスプロバイダは、まさにLaravelアプリケーションをブートストラップするための鍵となります。アプリケーション インスタンスが作成され、サービスプロバイダが登録され、リクエストがブートストラップされたアプリケーションに渡されます。本当に簡単です！

<!-- Having a firm grasp of how a Laravel application is built and bootstrapped via service providers is very valuable. Your application's user-defined service providers are stored in the `app/Providers` directory. -->
Laravel アプリケーションがどのように構築され、サービスプロバイダを介してブートストラップされるかをしっかりと把握することは非常に価値があります。アプリケーションのユーザー定義サービスプロバイダは、`app/Providers` ディレクトリに保存されます。

<!-- By default, the `AppServiceProvider` is fairly empty. This provider is a great place to add your application's own bootstrapping and service container bindings. For large applications, you may wish to create several service providers, each with more granular bootstrapping for specific services used by your application. -->
デフォルトでは、`AppServiceProvider` はかなり空です。このプロバイダは、アプリケーション独自のブートストラップとサービスコンテナー バインディングを追加するのに最適な場所です。大規模なアプリケーションの場合は、複数のサービスプロバイダを作成し、それぞれのサービスプロバイダで、アプリケーションで使用される特定のサービスをより詳細にブートストラップすることができます。

