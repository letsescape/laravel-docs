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
현실 세계에서 어떤 도구를 사용할 때, 그 도구가 어떻게 동작하는지 이해하면 더 자신감 있게 사용할 수 있습니다. 애플리케이션 개발도 마찬가지입니다. 개발 도구의 동작 원리를 알면 사용할 때 훨씬 더 편안하고 자신감이 생깁니다.

<!-- The goal of this document is to give you a good, high-level overview of how the Laravel framework works. By getting to know the overall framework better, everything feels less "magical" and you will be more confident building your applications. If you don't understand all of the terms right away, don't lose heart! Just try to get a basic grasp of what is going on, and your knowledge will grow as you explore other sections of the documentation. -->
이 문서의 목적은 Laravel 프레임워크가 전반적으로 어떻게 작동하는지 높은 수준에서 이해할 수 있도록 안내하는 데 있습니다. 전체적인 구조를 알고 나면, 모든 것이 마치 '마법'처럼 느껴지던 부분이 분명해지고, 자신의 애플리케이션을 만드는 데 더 큰 확신을 가질 수 있게 됩니다. 혹시 처음 보는 용어들이 많아도 너무 걱정하지 마십시오! 전반적인 흐름만 잡아두었다가, 다른 문서를 살펴보면서 자연스럽게 더 깊이 이해하게 될 것입니다.

<a name="lifecycle-overview"></a>
<!-- ## Lifecycle Overview -->
## Lifecycle Overview

<a name="first-steps"></a>
<!-- ### First Steps -->
### First Steps

<!-- The entry point for all requests to a Laravel application is the `public/index.php` file. All requests are directed to this file by your web server (Apache / Nginx) configuration. The `index.php` file doesn't contain much code. Rather, it is a starting point for loading the rest of the framework. -->
Laravel 애플리케이션으로 들어오는 모든 요청의 진입점(entry point)은 `public/index.php` 파일입니다. 웹 서버(Apache / Nginx) 설정을 통해 모든 요청이 이 파일로 들어오게 됩니다. `index.php` 파일 자체에는 코드가 많지 않습니다. 이 파일은 프레임워크의 나머지 부분을 불러오는 시작점 역할을 합니다.

<!-- The `index.php` file loads the Composer generated autoloader definition, and then retrieves an instance of the Laravel application from `bootstrap/app.php`. The first action taken by Laravel itself is to create an instance of the application / [service container](/docs/11.x/container). -->
`index.php` 파일에서는 Composer가 생성한 오토로더(autoload) 정의를 불러오고, `bootstrap/app.php`에서 Laravel 애플리케이션 인스턴스를 가져옵니다. Laravel이 처음으로 수행하는 일은 애플리케이션 인스턴스, 즉 [service container](/docs/11.x/container)를 생성하는 것입니다.

<a name="http-console-kernels"></a>
<!-- ### HTTP / Console Kernels -->
### HTTP / Console Kernels

<!-- Next, the incoming request is sent to either the HTTP kernel or the console kernel, using the `handleRequest` or `handleCommand` methods of the application instance, depending on the type of request entering the application. These two kernels serve as the central location through which all requests flow. For now, let's just focus on the HTTP kernel, which is an instance of `Illuminate\Foundation\Http\Kernel`. -->
그 다음, 들어온 요청은 애플리케이션 인스턴스의 `handleRequest` 또는 `handleCommand` 메서드를 사용해 HTTP 커널 또는 콘솔 커널로 전달됩니다. 어떤 커널로 전달되는지는 들어오는 요청의 타입에 따라 결정됩니다. 이 두 커널은 모든 요청이 흐르는 중심 역할을 합니다. 여기서는 우선 HTTP 커널에 대해서만 집중해보겠습니다. HTTP 커널은 `Illuminate\Foundation\Http\Kernel`의 인스턴스입니다.

<!-- The HTTP kernel defines an array of `bootstrappers` that will be run before the request is executed. These bootstrappers configure error handling, configure logging, [detect the application environment](/docs/11.x/configuration#environment-configuration), and perform other tasks that need to be done before the request is actually handled. Typically, these classes handle internal Laravel configuration that you do not need to worry about. -->
HTTP 커널은 요청이 실제로 실행되기 전에 동작해야 하는 `bootstrappers` 배열을 정의합니다. 이 부트스트래퍼들은 에러 핸들링 설정, 로깅 설정, [detect the application environment](/docs/11.x/configuration#environment-configuration) 등 요청이 처리되기 전에 필요한 여러 작업을 수행합니다. 일반적으로 이 클래스들은 Laravel 내부의 설정을 담당하므로, 여러분이 직접 신경쓸 필요는 없습니다.

<!-- The HTTP kernel is also responsible for passing the request through the application's middleware stack. These middleware handle reading and writing the [HTTP session](/docs/11.x/session), determining if the application is in maintenance mode, [verifying the CSRF token](/docs/11.x/csrf), and more. We'll talk more about these soon. -->
HTTP 커널은 또 애플리케이션의 미들웨어 스택을 통해 요청을 전달하는 역할을 합니다. 이 미들웨어들은 [HTTP session](/docs/11.x/session) 읽기·쓰기, 애플리케이션의 유지보수 모드 진입 여부 확인, [verifying the CSRF token](/docs/11.x/csrf) 등 여러 작업을 처리합니다. 이 내용은 곧 더 자세히 다루겠습니다.

<!-- The method signature for the HTTP kernel's `handle` method is quite simple: it receives a `Request` and returns a `Response`. Think of the kernel as being a big black box that represents your entire application. Feed it HTTP requests and it will return HTTP responses. -->
HTTP 커널의 `handle` 메서드 시그니처는 매우 단순합니다. 이 메서드는 `Request`를 받아서 `Response`를 반환합니다. 커널을 여러분의 전체 애플리케이션을 대표하는 ‘큰 블랙박스’라고 생각해보십시오. HTTP 요청을 입력하면 HTTP 응답을 출력합니다.

<a name="service-providers"></a>
<!-- ### Service Providers -->
### Service Providers

<!-- One of the most important kernel bootstrapping actions is loading the [service providers](/docs/11.x/providers) for your application. Service providers are responsible for bootstrapping all of the framework's various components, such as the database, queue, validation, and routing components. -->
커널 부트스트래핑 단계에서 가장 중요한 일 중 하나는 애플리케이션의 [service providers](/docs/11.x/providers)를 불러오는 것입니다. 서비스 프로바이더는 데이터베이스, 큐, 유효성 검증, 라우팅 등 프레임워크의 다양한 구성요소의 부트스트래핑을 담당합니다.

<!-- Laravel will iterate through this list of providers and instantiate each of them. After instantiating the providers, the `register` method will be called on all of the providers. Then, once all of the providers have been registered, the `boot` method will be called on each provider. This is so service providers may depend on every container binding being registered and available by the time their `boot` method is executed. -->
Laravel은 이 프로바이더 목록을 차례로 순회하며 각각을 인스턴스화합니다. 인스턴스화가 끝나면 모든 프로바이더의 `register` 메서드를 호출합니다. 그리고 모든 프로바이더가 등록(register)된 후에는 각 프로바이더의 `boot` 메서드가 호출됩니다. 이는 서비스 프로바이더의 `boot` 메서드가 실행될 때, 모든 컨테이너 바인딩이 이미 등록되고 사용할 수 있도록 보장하기 위함입니다.

<!-- Essentially every major feature offered by Laravel is bootstrapped and configured by a service provider. Since they bootstrap and configure so many features offered by the framework, service providers are the most important aspect of the entire Laravel bootstrap process. -->
Laravel에서 제공하는 주요 기능들은 대부분 서비스 프로바이더를 통해 부트스트랩 및 설정이 이루어집니다. 프레임워크의 다양한 기능들이 서비스 프로바이더에서 초기화되고 설정되므로, 서비스 프로바이더는 Laravel 부트스트랩 과정에서 가장 중요한 부분이라고 할 수 있습니다.

<!-- While the framework internally uses dozens of service providers, you also have the option to create your own. You can find a list of the user-defined or third-party service providers that your application is using in the `bootstrap/providers.php` file. -->
Laravel은 내부적으로 수십 개의 서비스 프로바이더를 사용하지만, 여러분이 직접 정의하거나 서드파티에서 제공하는 서비스 프로바이더도 추가할 수 있습니다. 애플리케이션에서 사용 중인 사용자 정의 또는 서드파티 서비스 프로바이더 목록은 `bootstrap/providers.php` 파일에서 확인할 수 있습니다.

<a name="routing"></a>
<!-- ### Routing -->
### Routing

<!-- Once the application has been bootstrapped and all service providers have been registered, the `Request` will be handed off to the router for dispatching. The router will dispatch the request to a route or controller, as well as run any route specific middleware. -->
애플리케이션 부트스트래핑이 모두 이뤄지고, 모든 서비스 프로바이더가 등록되면, 이제 `Request`가 라우터(router)로 전달되어 실제 디스패칭(dispatching)이 일어납니다. 라우터는 요청을 라우트 또는 컨트롤러에 연결하고, 해당 라우트에 지정된 미들웨어들도 실행합니다.

<!-- Middleware provide a convenient mechanism for filtering or examining HTTP requests entering your application. For example, Laravel includes a middleware that verifies if the user of your application is authenticated. If the user is not authenticated, the middleware will redirect the user to the login screen. However, if the user is authenticated, the middleware will allow the request to proceed further into the application. Some middleware are assigned to all routes within the application, like `PreventRequestsDuringMaintenance`, while some are only assigned to specific routes or route groups. You can learn more about middleware by reading the complete [middleware documentation](/docs/11.x/middleware). -->
미들웨어는 애플리케이션에 들어오는 HTTP 요청을 필터링하거나 검사하는 편리한 메커니즘을 제공합니다. 예를 들어, Laravel에는 사용자가 인증되었는지 확인하는 미들웨어가 있습니다. 인증되지 않은 사용자는 로그인 화면으로 리다이렉트되고, 인증된 사용자는 요청이 애플리케이션 내부로 계속 진행될 수 있습니다. 어떤 미들웨어는 애플리케이션의 모든 라우트에 할당되지만(예: `PreventRequestsDuringMaintenance`), 어떤 미들웨어는 특정 라우트나 라우트 그룹에만 할당될 수 있습니다. 미들웨어에 대해 더 깊이 알고 싶다면 [middleware documentation](/docs/11.x/middleware)를 참고하세요.

<!-- If the request passes through all of the matched route's assigned middleware, the route or controller method will be executed and the response returned by the route or controller method will be sent back through the route's chain of middleware. -->
요청이 매칭된 라우트의 미들웨어를 모두 통과하면, 해당 라우트나 컨트롤러의 메서드가 실행됩니다. 그리고 이 메서드가 반환한 응답은 다시 라우트의 미들웨어 체인을 거쳐 사용자에게 전달됩니다.

<a name="finishing-up"></a>
<!-- ### Finishing Up -->
### Finishing Up

<!-- Once the route or controller method returns a response, the response will travel back outward through the route's middleware, giving the application a chance to modify or examine the outgoing response. -->
라우트 또는 컨트롤러의 메서드가 응답을 반환하면, 그 응답은 라우트에 할당된 미들웨어들을 역으로 거치며 애플리케이션은 응답을 수정하거나 검사할 기회를 다시 가지게 됩니다.

<!-- Finally, once the response travels back through the middleware, the HTTP kernel's `handle` method returns the response object to the `handleRequest` of the application instance, and this method calls the `send` method on the returned response. The `send` method sends the response content to the user's web browser. We've now completed our journey through the entire Laravel request lifecycle! -->
마지막으로, 응답이 미들웨어를 모두 거치면 HTTP 커널의 `handle` 메서드는 이 응답 객체를 애플리케이션 인스턴스의 `handleRequest`로 반환하고, 이 메서드는 반환받은 응답 객체의 `send` 메서드를 호출합니다. `send` 메서드는 응답 내용을 사용자의 웹 브라우저로 전송합니다. 이로써 Laravel 요청 라이프사이클의 모든 과정을 마치게 됩니다!

<a name="focus-on-service-providers"></a>
<!-- ## Focus on Service Providers -->
## Focus on Service Providers

<!-- Service providers are truly the key to bootstrapping a Laravel application. The application instance is created, the service providers are registered, and the request is handed to the bootstrapped application. It's really that simple! -->
서비스 프로바이더는 Laravel 애플리케이션의 부트스트래핑에 있어서 핵심적인 역할을 합니다. 애플리케이션 인스턴스가 생성되고, 서비스 프로바이더가 등록된 후에 비로소 요청이 부트스트랩된 애플리케이션에 전달됩니다. 정말 이만큼 간단합니다!

<!-- Having a firm grasp of how a Laravel application is built and bootstrapped via service providers is very valuable. Your application's user-defined service providers are stored in the `app/Providers` directory. -->
서비스 프로바이더를 통해 Laravel 애플리케이션이 어떻게 구성되고 부트스트랩되는지 확실히 이해하는 것은 매우 큰 도움이 됩니다. 애플리케이션에서 직접 정의한 서비스 프로바이더는 `app/Providers` 디렉터리에 저장되어 있습니다.

<!-- By default, the `AppServiceProvider` is fairly empty. This provider is a great place to add your application's own bootstrapping and service container bindings. For large applications, you may wish to create several service providers, each with more granular bootstrapping for specific services used by your application. -->
기본적으로 `AppServiceProvider`는 거의 비어 있습니다. 이 프로바이더는 여러분의 애플리케이션만의 부트스트래핑 작업이나 서비스 컨테이너 바인딩을 추가하기에 적합한 위치입니다. 애플리케이션 규모가 크다면, 각 서비스별로 더욱 세분화된 부트스트래핑을 담당하는 여러 개의 서비스 프로바이더를 만들 수도 있습니다.