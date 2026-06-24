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
"실제 환경"에서 어떤 도구를 사용할 때, 그 도구가 어떻게 동작하는지 이해하면 더 자신감을 갖게 됩니다. 애플리케이션 개발도 마찬가지입니다. 개발 도구가 어떻게 작동하는지 알면 더 편안하고 자신 있게 도구를 사용할 수 있습니다.

<!-- The goal of this document is to give you a good, high-level overview of how the Laravel framework works. By getting to know the overall framework better, everything feels less "magical" and you will be more confident building your applications. If you don't understand all of the terms right away, don't lose heart! Just try to get a basic grasp of what is going on, and your knowledge will grow as you explore other sections of the documentation. -->
이 문서의 목표는 Laravel 프레임워크가 어떻게 작동하는지에 대한 전체적인 개념을 고수준에서 이해할 수 있도록 돕는 것입니다. 프레임워크 전체를 더 잘 알게 되면 모든 것이 덜 '마법처럼' 느껴지고 애플리케이션을 구축하는 데 더 자신감이 생깁니다. 처음에 모든 용어를 완벽히 이해하지 못하더라도 낙담하지 마세요! 우선 전반적으로 어떤 일이 일어나는지 기본 개념을 파악하려고 노력하면, 문서의 다른 부분을 살펴보면서 자연스럽게 지식이 쌓일 것입니다.

<a name="lifecycle-overview"></a>
<!-- ## Lifecycle Overview -->
## Lifecycle Overview

<a name="first-steps"></a>
<!-- ### First Steps -->
### First Steps

<!-- The entry point for all requests to a Laravel application is the `public/index.php` file. All requests are directed to this file by your web server (Apache / Nginx) configuration. The `index.php` file doesn't contain much code. Rather, it is a starting point for loading the rest of the framework. -->
Laravel 애플리케이션으로 들어오는 모든 요청의 진입점은 `public/index.php` 파일입니다. 모든 요청은 웹 서버(Apache / Nginx)의 설정에 의해 이 파일로 전달됩니다. `index.php` 파일 자체에는 많은 코드가 포함되어 있지 않습니다. 대신 나머지 프레임워크를 로드하는 시작점 역할을 합니다.

<!-- The `index.php` file loads the Composer generated autoloader definition, and then retrieves an instance of the Laravel application from `bootstrap/app.php`. The first action taken by Laravel itself is to create an instance of the application / [service container](/docs/master/container). -->
`index.php` 파일은 Composer가 생성한 오토로더 정의를 불러오고, `bootstrap/app.php`에서 Laravel 애플리케이션 인스턴스를 가져옵니다. Laravel이 가장 먼저 하는 작업은 애플리케이션 / [service container](/docs/master/container) 인스턴스를 생성하는 것입니다.

<a name="http-console-kernels"></a>
<!-- ### HTTP / Console Kernels -->
### HTTP / Console Kernels

<!-- Next, the incoming request is sent to either the HTTP kernel or the console kernel, using the `handleRequest` or `handleCommand` methods of the application instance, depending on the type of request entering the application. These two kernels serve as the central location through which all requests flow. For now, let's just focus on the HTTP kernel, which is an instance of `Illuminate\Foundation\Http\Kernel`. -->
다음으로, 들어오는 요청은 애플리케이션 인스턴스의 `handleRequest` 또는 `handleCommand` 메서드를 통해 각각 HTTP 커널 또는 콘솔 커널로 전달됩니다. 이는 요청 유형에 따라 달라집니다. 이 두 커널은 모든 요청이 흐르는 중앙 허브 역할을 합니다. 여기서는 HTTP 커널에 집중해 보겠습니다. HTTP 커널은 `Illuminate\Foundation\Http\Kernel` 클래스의 인스턴스입니다.

<!-- The HTTP kernel defines an array of `bootstrappers` that will be run before the request is executed. These bootstrappers configure error handling, configure logging, [detect the application environment](/docs/master/configuration#environment-configuration), and perform other tasks that need to be done before the request is actually handled. Typically, these classes handle internal Laravel configuration that you do not need to worry about. -->
HTTP 커널은 요청이 처리되기 전에 실행될 `bootstrappers` 배열을 정의합니다. 이 부트스트래퍼들은 오류 처리 설정, 로그 설정, [detect the application environment](/docs/master/configuration#environment-configuration)와 같이 요청 처리 전에 필요한 여러 작업을 수행합니다. 일반적으로 이 클래스들은 Laravel 내부 설정을 처리하며, 여러분이 직접 신경 쓸 부분은 아닙니다.

<!-- The HTTP kernel is also responsible for passing the request through the application's middleware stack. These middleware handle reading and writing the [HTTP session](/docs/master/session), determining if the application is in maintenance mode, [verifying the CSRF token](/docs/master/csrf), and more. We'll talk more about these soon. -->
또한 HTTP 커널은 요청을 애플리케이션의 미들웨어 스택으로 전달하는 역할도 합니다. 이 미들웨어들은 [HTTP session](/docs/master/session)을 읽고 쓰는 작업, 애플리케이션이 유지보수 모드인지 확인, [verifying the CSRF token](/docs/master/csrf) 등 다양한 역할을 수행합니다. 이런 부분들은 곧 더 자세히 설명할 예정입니다.

<!-- The method signature for the HTTP kernel's `handle` method is quite simple: it receives a `Request` and returns a `Response`. Think of the kernel as being a big black box that represents your entire application. Feed it HTTP requests and it will return HTTP responses. -->
HTTP 커널의 `handle` 메서드 시그니처는 매우 간단합니다: `Request` 객체를 받아 `Response` 객체를 반환합니다. 커널은 여러분의 애플리케이션 전체를 대표하는 큰 블랙박스 같은 역할을 한다고 생각하면 됩니다. HTTP 요청을 넣으면 HTTP 응답을 내보내죠.

<a name="service-providers"></a>
<!-- ### Service Providers -->
### Service Providers

<!-- One of the most important kernel bootstrapping actions is loading the [service providers](/docs/master/providers) for your application. Service providers are responsible for bootstrapping all of the framework's various components, such as the database, queue, validation, and routing components. -->
커널 부트스트래핑 과정에서 가장 중요한 작업 중 하나는 애플리케이션의 [service providers](/docs/master/providers)를 로드하는 것입니다. 서비스 프로바이더는 데이터베이스, 큐, 유효성 검사, 라우팅 등 프레임워크의 다양한 구성 요소들을 부트스트랩하는 역할을 담당합니다.

<!-- Laravel will iterate through this list of providers and instantiate each of them. After instantiating the providers, the `register` method will be called on all of the providers. Then, once all of the providers have been registered, the `boot` method will be called on each provider. This is so service providers may depend on every container binding being registered and available by the time their `boot` method is executed. -->
Laravel은 서비스 프로바이더 리스트를 순회하면서 각 프로바이더를 인스턴스화합니다. 프로바이더 인스턴스가 생성되면, 모든 프로바이더에 대해 `register` 메서드가 호출됩니다. 그 다음 등록이 완료된 모든 프로바이더에 대해 `boot` 메서드가 호출됩니다. 이렇게 하는 이유는 모든 컨테이너 바인딩이 등록 완료된 후에 `boot` 메서드가 실행되도록 해 서비스 프로바이더들이 서로 의존할 수 있게 하려는 것입니다.

<!-- Essentially every major feature offered by Laravel is bootstrapped and configured by a service provider. Since they bootstrap and configure so many features offered by the framework, service providers are the most important aspect of the entire Laravel bootstrap process. -->
Laravel이 제공하는 거의 모든 주요 기능은 서비스 프로바이더를 통해 부트스트랩되고 설정됩니다. 프레임워크가 제공하는 수많은 기능을 부트스트랩하고 구성하기 때문에, 서비스 프로바이더는 전체 Laravel 부트스트랩 과정에서 가장 중요한 부분입니다.

<!-- While the framework internally uses dozens of service providers, you also have the option to create your own. You can find a list of the user-defined or third-party service providers that your application is using in the `bootstrap/providers.php` file. -->
내부적으로 수십 개의 서비스 프로바이더를 사용하지만, 여러분도 직접 서비스 프로바이더를 만들어 사용할 수 있습니다. 여러분의 애플리케이션에서 사용 중인 사용자 정의 또는 서드파티 서비스 프로바이더 목록은 `bootstrap/providers.php` 파일에서 확인할 수 있습니다.

<a name="routing"></a>
<!-- ### Routing -->
### Routing

<!-- Once the application has been bootstrapped and all service providers have been registered, the `Request` will be handed off to the router for dispatching. The router will dispatch the request to a route or controller, as well as run any route specific middleware. -->
애플리케이션이 부트스트랩되고 모든 서비스 프로바이더가 등록되면, `Request`는 라우터에게 전달되어 요청을 디스패치합니다. 라우터는 요청을 라우트나 컨트롤러로 전달하고, 라우트에 지정된 미들웨어를 실행합니다.

<!-- Middleware provide a convenient mechanism for filtering or examining HTTP requests entering your application. For example, Laravel includes a middleware that verifies if the user of your application is authenticated. If the user is not authenticated, the middleware will redirect the user to the login screen. However, if the user is authenticated, the middleware will allow the request to proceed further into the application. Some middleware are assigned to all routes within the application, like `PreventRequestsDuringMaintenance`, while some are only assigned to specific routes or route groups. You can learn more about middleware by reading the complete [middleware documentation](/docs/master/middleware). -->
미들웨어는 애플리케이션으로 들어오는 HTTP 요청을 필터링하거나 검사하는 편리한 메커니즘을 제공합니다. 예를 들어, Laravel에는 사용자가 인증되었는지 확인하는 미들웨어가 포함되어 있습니다. 인증이 되어 있지 않으면 이 미들웨어는 사용자를 로그인 화면으로 리다이렉트합니다. 인증된 경우 요청이 애플리케이션 내부로 계속 진행됩니다. 어떤 미들웨어는 `PreventRequestsDuringMaintenance`처럼 애플리케이션 내 모든 라우트에 할당되어 있고, 어떤 미들웨어는 특정 라우트나 라우트 그룹에만 할당되어 있습니다. 미들웨어에 대한 자세한 내용은 전체 [middleware documentation](/docs/master/middleware)를 참고하세요.

<!-- If the request passes through all of the matched route's assigned middleware, the route or controller method will be executed and the response returned by the route or controller method will be sent back through the route's chain of middleware. -->
요청이 매칭된 라우트에 할당된 모든 미들웨어를 통과하면, 라우트 또는 컨트롤러 메서드가 실행되고, 이 메서드가 반환하는 응답은 다시 라우트의 미들웨어 체인을 거쳐 전송됩니다.

<a name="finishing-up"></a>
<!-- ### Finishing Up -->
### Finishing Up

<!-- Once the route or controller method returns a response, the response will travel back outward through the route's middleware, giving the application a chance to modify or examine the outgoing response. -->
라우트 또는 컨트롤러 메서드가 응답을 반환하면, 응답은 라우트의 미들웨어를 거슬러 다시 전달됩니다. 이를 통해 애플리케이션이 나가는 응답을 수정하거나 검사할 기회를 가집니다.

<!-- Finally, once the response travels back through the middleware, the HTTP kernel's `handle` method returns the response object to the `handleRequest` of the application instance, and this method calls the `send` method on the returned response. The `send` method sends the response content to the user's web browser. We've now completed our journey through the entire Laravel request lifecycle! -->
마지막으로, 응답이 미들웨어를 모두 통과하면 HTTP 커널의 `handle` 메서드는 응답 객체를 애플리케이션 인스턴스의 `handleRequest`로 반환하고, 해당 메서드는 반환된 응답의 `send` 메서드를 호출합니다. `send` 메서드는 응답 내용을 사용자의 웹 브라우저로 전송합니다. 이렇게 해서 Laravel 요청 생명주기를 완벽히 마친 것입니다!

<a name="focus-on-service-providers"></a>
<!-- ## Focus on Service Providers -->
## Focus on Service Providers

<!-- Service providers are truly the key to bootstrapping a Laravel application. The application instance is created, the service providers are registered, and the request is handed to the bootstrapped application. It's really that simple! -->
서비스 프로바이더는 Laravel 애플리케이션을 부트스트랩하는 핵심입니다. 애플리케이션 인스턴스가 생성되고, 서비스 프로바이더들이 등록되며, 부트스트랩된 애플리케이션에 요청이 전달됩니다. 정말 그만큼 단순합니다!

<!-- Having a firm grasp of how a Laravel application is built and bootstrapped via service providers is very valuable. Your application's user-defined service providers are stored in the `app/Providers` directory. -->
Laravel 애플리케이션이 어떻게 구축되고 서비스 프로바이더를 통해 부트스트랩되는지 확실히 이해하는 것은 매우 중요합니다. 여러분이 직접 정의하는 서비스 프로바이더들은 `app/Providers` 디렉토리에 저장됩니다.

<!-- By default, the `AppServiceProvider` is fairly empty. This provider is a great place to add your application's own bootstrapping and service container bindings. For large applications, you may wish to create several service providers, each with more granular bootstrapping for specific services used by your application. -->
기본적으로 `AppServiceProvider`는 꽤 비어 있는 상태입니다. 이 프로바이더는 여러분 애플리케이션만의 부트스트랩 작업과 서비스 컨테이너 바인딩을 추가하기에 좋은 장소입니다. 대규모 애플리케이션의 경우, 특정 서비스별로 더 세분화된 부트스트랩 작업을 처리하는 여러 서비스 프로바이더를 만드는 것이 좋습니다.