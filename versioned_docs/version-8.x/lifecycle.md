<!-- # Request Lifecycle -->
# Request Lifecycle

- [Introduction](#introduction)
- [Lifecycle Overview](#lifecycle-overview)
    - [First Steps](#first-steps)
    - [HTTP / Console Kernels](#http-console-kernels)
    - [Service Providers](#service-providers)
    - [Routing](#routing)
    - [Finishing Up](#finishing-up)
- [Focus On Service Providers](#focus-on-service-providers)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- When using any tool in the "real world", you feel more confident if you understand how that tool works. Application development is no different. When you understand how your development tools function, you feel more comfortable and confident using them. -->
"실제 세계"에서 어떤 도구를 사용할 때, 그 도구가 어떻게 동작하는지 이해하면 더욱 자신감 있게 사용할 수 있습니다. 애플리케이션 개발도 마찬가지입니다. 개발 도구의 작동 원리를 이해하면, 도구를 사용할 때 더 편안하고 확신을 가질 수 있습니다.

<!-- The goal of this document is to give you a good, high-level overview of how the Laravel framework works. By getting to know the overall framework better, everything feels less "magical" and you will be more confident building your applications. If you don't understand all of the terms right away, don't lose heart! Just try to get a basic grasp of what is going on, and your knowledge will grow as you explore other sections of the documentation. -->
이 문서의 목표는 Laravel 프레임워크가 어떻게 동작하는지에 대한 높은 수준의 개요를 제공하는 것입니다. 전체적인 동작 흐름을 이해하면, Laravel이 덜 "마법"처럼 느껴지고 여러분이 직접 애플리케이션을 만들 때 더 큰 자신감을 갖게 됩니다. 혹시 모든 용어가 당장 이해되지 않더라도 걱정하지 마세요! 전체적으로 어떤 일이 벌어지는지 기본적인 흐름만 파악해도 괜찮으며, 문서의 다른 섹션을 읽으며 점차 지식을 쌓아갈 수 있습니다.

<a name="lifecycle-overview"></a>
<!-- ## Lifecycle Overview -->
## Lifecycle Overview

<a name="first-steps"></a>
<!-- ### First Steps -->
### First Steps

<!-- The entry point for all requests to a Laravel application is the `public/index.php` file. All requests are directed to this file by your web server (Apache / Nginx) configuration. The `index.php` file doesn't contain much code. Rather, it is a starting point for loading the rest of the framework. -->
Laravel 애플리케이션의 모든 요청은 `public/index.php` 파일을 진입점으로 합니다. 웹 서버(Apache / Nginx) 설정에 의해 모든 요청이 이 파일로 연결됩니다. `index.php` 파일 자체에는 복잡한 코드가 많지 않으며, 프레임워크의 나머지 부분을 불러들이는 출발점 역할을 합니다.

<!-- The `index.php` file loads the Composer generated autoloader definition, and then retrieves an instance of the Laravel application from `bootstrap/app.php`. The first action taken by Laravel itself is to create an instance of the application / [service container](/docs/8.x/container). -->
`index.php` 파일은 Composer가 생성한 오토로더 정의를 불러오고, 그 다음에 `bootstrap/app.php`에서 Laravel 애플리케이션 인스턴스를 가져옵니다. Laravel이 처음으로 수행하는 작업은 애플리케이션(및 [service container](/docs/8.x/container)) 인스턴스를 생성하는 것입니다.

<a name="http-console-kernels"></a>
<!-- ### HTTP / Console Kernels -->
### HTTP / Console Kernels

<!-- Next, the incoming request is sent to either the HTTP kernel or the console kernel, depending on the type of request that is entering the application. These two kernels serve as the central location that all requests flow through. For now, let's just focus on the HTTP kernel, which is located in `app/Http/Kernel.php`. -->
그 다음, 들어오는 요청이 어떤 종류인지에 따라 HTTP 커널 또는 콘솔 커널로 전달됩니다. 이 두 커널은 모든 요청이 반드시 통과하는 중앙 허브 역할을 합니다. 지금은 HTTP 커널에 집중해보겠습니다. 이 커널의 위치는 `app/Http/Kernel.php`입니다.

<!-- The HTTP kernel extends the `Illuminate\Foundation\Http\Kernel` class, which defines an array of `bootstrappers` that will be run before the request is executed. These bootstrappers configure error handling, configure logging, [detect the application environment](/docs/8.x/configuration#environment-configuration), and perform other tasks that need to be done before the request is actually handled. Typically, these classes handle internal Laravel configuration that you do not need to worry about. -->
HTTP 커널은 `Illuminate\Foundation\Http\Kernel` 클래스를 확장하며, 이 클래스에는 요청 실행 전에 반드시 실행해야 하는 `bootstrappers`라는 배열이 정의되어 있습니다. 이 부트스트래퍼는 오류 처리 설정, 로깅 설정, [detect the application environment](/docs/8.x/configuration#environment-configuration) 등 요청이 실제로 처리되기 전에 필요한 여러 작업을 수행합니다. 대부분의 경우 이 클래스들은 내부적인 Laravel 설정을 담당하므로, 개발자가 따로 신경 쓸 필요는 없습니다.

<!-- The HTTP kernel also defines a list of HTTP [middleware](/docs/8.x/middleware) that all requests must pass through before being handled by the application. These middleware handle reading and writing the [HTTP session](/docs/8.x/session), determining if the application is in maintenance mode, [verifying the CSRF token](/docs/8.x/csrf), and more. We'll talk more about these soon. -->
또한, HTTP 커널에는 모든 요청이 애플리케이션에서 처리되기 전에 통과하게 되는 HTTP [middleware](/docs/8.x/middleware) 목록도 정의되어 있습니다. 이 미들웨어는 [HTTP session](/docs/8.x/session) 읽기 및 쓰기, 애플리케이션이 유지보수 모드인지 판별, [verifying the CSRF token](/docs/8.x/csrf) 등 여러 역할을 수행합니다. 이 부분에 대해서는 곧 더 자세히 설명하겠습니다.

<!-- The method signature for the HTTP kernel's `handle` method is quite simple: it receives a `Request` and returns a `Response`. Think of the kernel as being a big black box that represents your entire application. Feed it HTTP requests and it will return HTTP responses. -->
HTTP 커널의 `handle` 메서드 시그니처는 매우 단순합니다. 이 메서드는 `Request`를 받아서 `Response`를 반환합니다. 커널을 여러분의 전체 애플리케이션을 대표하는 "큰 블랙박스"라고 생각해 보세요. HTTP 요청을 넣으면 HTTP 응답이 나옵니다.

<a name="service-providers"></a>
<!-- ### Service Providers -->
### Service Providers

<!-- One of the most important kernel bootstrapping actions is loading the [service providers](/docs/8.x/providers) for your application. All of the service providers for the application are configured in the `config/app.php` configuration file's `providers` array. -->
커널 부트스트래핑에서 가장 중요한 단계 중 하나는 애플리케이션의 [service providers](/docs/8.x/providers)를 로딩하는 것입니다. 애플리케이션의 모든 서비스 프로바이더는 `config/app.php` 설정 파일의 `providers` 배열에 등록되어 있습니다.

<!-- Laravel will iterate through this list of providers and instantiate each of them. After instantiating the providers, the `register` method will be called on all of the providers. Then, once all of the providers have been registered, the `boot` method will be called on each provider. This is so service providers may depend on every container binding being registered and available by the time their `boot` method is executed. -->
Laravel은 이 프로바이더 목록을 순회하면서 각 프로바이더를 인스턴스화합니다. 모든 프로바이더 인스턴스를 생성한 후에는 각 프로바이더의 `register` 메서드를 호출합니다. 그리고 모든 프로바이더가 등록된 후에는 각 프로바이더의 `boot` 메서드를 호출합니다. 이렇게 하는 이유는, 서비스 프로바이더의 `boot` 메서드가 실행될 때 컨테이너의 모든 바인딩이 이미 등록되어 사용할 수 있도록 보장하기 위함입니다.

<!-- Service providers are responsible for bootstrapping all of the framework's various components, such as the database, queue, validation, and routing components. Essentially every major feature offered by Laravel is bootstrapped and configured by a service provider. Since they bootstrap and configure so many features offered by the framework, service providers are the most important aspect of the entire Laravel bootstrap process. -->
서비스 프로바이더는 데이터베이스, 큐, 유효성 검증, 라우팅 등 다양한 프레임워크 핵심 컴포넌트들의 부트스트래핑을 책임집니다. 실제로 Laravel의 거의 모든 주요 기능은 서비스 프로바이더에 의해 초기화되고 설정됩니다. 이처럼 프레임워크의 다양한 기능을 부트스트래핑하고 설정하는 역할을 하기 때문에, 서비스 프로바이더는 Laravel 부트스트랩 과정에서 가장 중요한 부분이라 할 수 있습니다.

<a name="routing"></a>
<!-- ### Routing -->
### Routing

<!-- One of the most important service providers in your application is the `App\Providers\RouteServiceProvider`. This service provider loads the route files contained within your application's `routes` directory. Go ahead, crack open the `RouteServiceProvider` code and take a look at how it works! -->
여러분 애플리케이션에서 가장 중요한 서비스 프로바이더 중 하나는 `App\Providers\RouteServiceProvider`입니다. 이 서비스 프로바이더는 애플리케이션의 `routes` 디렉터리 내 라우트 파일들을 불러옵니다. 직접 `RouteServiceProvider` 코드를 열어보면서 어떻게 동작하는지 살펴보세요!

<!-- Once the application has been bootstrapped and all service providers have been registered, the `Request` will be handed off to the router for dispatching. The router will dispatch the request to a route or controller, as well as run any route specific middleware. -->
애플리케이션의 부트스트랩이 완료되고 모든 서비스 프로바이더가 등록된 후에는, 이제 `Request` 객체가 라우터로 전달되어 실제 디스패치가 이루어집니다. 라우터는 요청을 적절한 라우트나 컨트롤러로 전달하고, 각 라우트에 지정된 미들웨어를 실행시킵니다.

<!-- Middleware provide a convenient mechanism for filtering or examining HTTP requests entering your application. For example, Laravel includes a middleware that verifies if the user of your application is authenticated. If the user is not authenticated, the middleware will redirect the user to the login screen. However, if the user is authenticated, the middleware will allow the request to proceed further into the application. Some middleware are assigned to all routes within the application, like those defined in the `$middleware` property of your HTTP kernel, while some are only assigned to specific routes or route groups. You can learn more about middleware by reading the complete [middleware documentation](/docs/8.x/middleware). -->
미들웨어는 애플리케이션으로 들어오는 HTTP 요청을 필터링하거나 검사할 수 있는 편리한 메커니즘을 제공합니다. 예를 들어, Laravel에는 사용자가 인증되었는지 검증하는 미들웨어가 내장되어 있습니다. 만약 사용자가 인증되지 않았다면, 해당 미들웨어가 로그인 화면으로 리다이렉트합니다. 반대로, 사용자가 인증된 경우에는 요청이 애플리케이션의 더 깊은 영역으로 정상적으로 진행됩니다. 일부 미들웨어는 애플리케이션 내 모든 라우트에 적용되며(HTTP 커널의 `$middleware` 속성에 정의되어 있음), 어떤 미들웨어는 특정 라우트나 라우트 그룹에만 지정됩니다. 미들웨어에 대해 더 자세히 알고 싶다면 [middleware documentation](/docs/8.x/middleware)를 참고하세요.

<!-- If the request passes through all of the matched route's assigned middleware, the route or controller method will be executed and the response returned by the route or controller method will be sent back through the route's chain of middleware. -->
요청이 해당 라우트에 할당된 모든 미들웨어를 통과하면, 라우트나 컨트롤러의 메서드가 실행되고 그 반환값이 라우트의 미들웨어 체인을 따라 다시 응답으로 전송됩니다.

<a name="finishing-up"></a>
<!-- ### Finishing Up -->
### Finishing Up

<!-- Once the route or controller method returns a response, the response will travel back outward through the route's middleware, giving the application a chance to modify or examine the outgoing response. -->
라우트나 컨트롤러 메서드가 응답을 반환하면, 해당 응답은 다시 라우트의 미들웨어를 역방향으로 통과하면서, 애플리케이션이 반환되는 응답을 수정하거나 검사할 수 있는 기회가 주어집니다.

<!-- Finally, once the response travels back through the middleware, the HTTP kernel's `handle` method returns the response object and the `index.php` file calls the `send` method on the returned response. The `send` method sends the response content to the user's web browser. We've finished our journey through the entire Laravel request lifecycle! -->
마지막으로, 응답이 미들웨어를 모두 통과하면, HTTP 커널의 `handle` 메서드에서 응답 객체를 반환하고, `index.php` 파일이 반환된 응답에서 `send` 메서드를 호출합니다. 이 `send` 메서드는 실제로 응답 내용을 사용자의 웹 브라우저로 전송합니다. 이렇게 해서 Laravel의 전체 요청 라이프사이클을 모두 훑어보았습니다!

<a name="focus-on-service-providers"></a>
<!-- ## Focus On Service Providers -->
## Focus On Service Providers

<!-- Service providers are truly the key to bootstrapping a Laravel application. The application instance is created, the service providers are registered, and the request is handed to the bootstrapped application. It's really that simple! -->
서비스 프로바이더는 정말 Laravel 애플리케이션 부트스트래핑의 핵심입니다. 애플리케이션 인스턴스가 생성되고, 서비스 프로바이더가 등록되며, 이후 요청이 부트스트랩된 애플리케이션에 전달됩니다. 정말 이처럼 단순합니다!

<!-- Having a firm grasp of how a Laravel application is built and bootstrapped via service providers is very valuable. Your application's default service providers are stored in the `app/Providers` directory. -->
서비스 프로바이더를 통해 Laravel 애플리케이션이 어떻게 구성되고 부트스트랩되는지 제대로 이해하는 것은 매우 중요합니다. 여러분 애플리케이션의 기본 서비스 프로바이더들은 `app/Providers` 디렉터리에 저장되어 있습니다.

<!-- By default, the `AppServiceProvider` is fairly empty. This provider is a great place to add your application's own bootstrapping and service container bindings. For large applications, you may wish to create several service providers, each with more granular bootstrapping for specific services used by your application. -->
기본적으로 `AppServiceProvider`는 거의 비어 있습니다. 이 프로바이더는 여러분의 애플리케이션에서 고유한 부트스트래핑 코드나 서비스 컨테이너 바인딩을 추가하기에 좋은 위치입니다. 규모가 큰 애플리케이션에서는, 더 세부적인 서비스별로 여러 개의 서비스 프로바이더를 만들어 각각의 부트스트래핑을 별도로 관리할 수도 있습니다.
