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
실생활에서 어떤 도구를 쓸 때 그 도구가 어떻게 동작하는지 이해하면 훨씬 더 자신있게 사용할 수 있습니다. 애플리케이션 개발도 마찬가지입니다. 자신이 사용하는 개발 도구가 어떻게 작동하는지 알게 되면, 훨씬 더 편안하고 확신을 가지고 개발에 임할 수 있습니다.

<!-- The goal of this document is to give you a good, high-level overview of how the Laravel framework works. By getting to know the overall framework better, everything feels less "magical" and you will be more confident building your applications. If you don't understand all of the terms right away, don't lose heart! Just try to get a basic grasp of what is going on, and your knowledge will grow as you explore other sections of the documentation. -->
이 문서의 목적은 Laravel 프레임워크가 어떻게 동작하는지 전체적인 그림을 이해할 수 있도록 돕는 것입니다. 프레임워크의 구조를 잘 알게 되면, 내부 동작이 덜 '마법'처럼 느껴지고, 애플리케이션을 구축할 때 더 자신감을 얻을 수 있습니다. 혹시 처음에는 모든 용어가 이해되지 않는다 해도 걱정하지 마세요! 일단 전체 흐름을 파악하는 데 집중하시고, 다른 설명서를 읽어가며 점차 더 많은 내용을 이해하게 될 것입니다.

<a name="lifecycle-overview"></a>
<!-- ## Lifecycle Overview -->
## Lifecycle Overview

<a name="first-steps"></a>
<!-- ### First Steps -->
### First Steps

<!-- The entry point for all requests to a Laravel application is the `public/index.php` file. All requests are directed to this file by your web server (Apache / Nginx) configuration. The `index.php` file doesn't contain much code. Rather, it is a starting point for loading the rest of the framework. -->
Laravel 애플리케이션에 대한 모든 요청의 진입점은 바로 `public/index.php` 파일입니다. 모든 요청은 웹 서버(Apache나 Nginx)의 설정에 의해 이 파일로 전달됩니다. `index.php` 파일 자체는 많은 코드를 담고 있지 않고, 프레임워크의 나머지 부분을 불러오는 출발점 역할을 합니다.

<!-- The `index.php` file loads the Composer generated autoloader definition, and then retrieves an instance of the Laravel application from `bootstrap/app.php`. The first action taken by Laravel itself is to create an instance of the application / [service container](/docs/10.x/container). -->
이 `index.php` 파일은 Composer에서 생성된 오토로더 정의를 불러온 다음, `bootstrap/app.php`에서 Laravel 애플리케이션 인스턴스를 가져옵니다. Laravel이 가장 먼저 수행하는 동작은 애플리케이션, 즉 [service container](/docs/10.x/container)의 인스턴스를 만드는 것입니다.

<a name="http-console-kernels"></a>
<!-- ### HTTP / Console Kernels -->
### HTTP / Console Kernels

<!-- Next, the incoming request is sent to either the HTTP kernel or the console kernel, depending on the type of request that is entering the application. These two kernels serve as the central location that all requests flow through. For now, let's just focus on the HTTP kernel, which is located in `app/Http/Kernel.php`. -->
그 다음에는 들어온 요청의 종류에 따라 HTTP 커널 또는 콘솔 커널로 해당 요청이 전달됩니다. 이 두 커널은 모든 요청이 반드시 거치는 중앙 허브 역할을 합니다. 여기서는 우선 `app/Http/Kernel.php`에 위치한 HTTP 커널에 집중하여 살펴보겠습니다.

<!-- The HTTP kernel extends the `Illuminate\Foundation\Http\Kernel` class, which defines an array of `bootstrappers` that will be run before the request is executed. These bootstrappers configure error handling, configure logging, [detect the application environment](/docs/10.x/configuration#environment-configuration), and perform other tasks that need to be done before the request is actually handled. Typically, these classes handle internal Laravel configuration that you do not need to worry about. -->
HTTP 커널은 `Illuminate\Foundation\Http\Kernel` 클래스를 확장하며, 이 클래스에는 요청이 실행되기 전에 동작하는 `bootstrappers` 배열이 정의되어 있습니다. 이 부트스트래퍼들은 에러 핸들링 설정, 로깅 설정, [detect the application environment](/docs/10.x/configuration#environment-configuration) 등, 요청을 실제로 처리하기 전에 필요한 여러 작업들을 수행합니다. 이러한 클래스들은 대부분 Laravel 내부 설정에 관련된 것이라, 일반적으로 개발자가 직접 신경쓸 필요는 없습니다.

<!-- The HTTP kernel also defines a list of HTTP [middleware](/docs/10.x/middleware) that all requests must pass through before being handled by the application. These middleware handle reading and writing the [HTTP session](/docs/10.x/session), determining if the application is in maintenance mode, [verifying the CSRF token](/docs/10.x/csrf), and more. We'll talk more about these soon. -->
또한 HTTP 커널에는 애플리케이션으로 들어오는 모든 요청이 반드시 통과해야 하는 HTTP [middleware](/docs/10.x/middleware) 리스트도 정의되어 있습니다. 이 미들웨어들은 [HTTP session](/docs/10.x/session)을 읽고 쓰거나, 애플리케이션이 유지보수 모드인지 확인하거나, [verifying the CSRF token](/docs/10.x/csrf)하는 등 여러 가지 역할을 맡습니다. 이 내용들은 뒤에서 더 자세히 설명합니다.

<!-- The method signature for the HTTP kernel's `handle` method is quite simple: it receives a `Request` and returns a `Response`. Think of the kernel as being a big black box that represents your entire application. Feed it HTTP requests and it will return HTTP responses. -->
HTTP 커널의 `handle` 메서드 시그니처는 상당히 단순합니다. `Request`를 받아서 `Response`를 반환합니다. 커널은 마치 애플리케이션 전체를 하나의 거대한 블랙박스처럼 생각하면 됩니다. 이 커널에 HTTP 요청을 전달하면, HTTP 응답을 돌려받게 됩니다.

<a name="service-providers"></a>
<!-- ### Service Providers -->
### Service Providers

<!-- One of the most important kernel bootstrapping actions is loading the [service providers](/docs/10.x/providers) for your application. Service providers are responsible for bootstrapping all of the framework's various components, such as the database, queue, validation, and routing components. All of the service providers for the application are configured in the `config/app.php` configuration file's `providers` array. -->
커널에서 부트스트래핑 작업 중 가장 중요한 일 중 하나가 바로 애플리케이션의 [service providers](/docs/10.x/providers)를 로드하는 것입니다. 서비스 프로바이더는 데이터베이스, 큐, 유효성 검증, 라우팅과 같은 프레임워크의 다양한 구성요소를 부트스트랩하는 역할을 담당합니다. 애플리케이션에 사용되는 모든 서비스 프로바이더는 `config/app.php` 설정 파일의 `providers` 배열에 등록되어 있습니다.

<!-- Laravel will iterate through this list of providers and instantiate each of them. After instantiating the providers, the `register` method will be called on all of the providers. Then, once all of the providers have been registered, the `boot` method will be called on each provider. This is so service providers may depend on every container binding being registered and available by the time their `boot` method is executed. -->
Laravel은 이 프로바이더 리스트를 하나씩 순회하며 인스턴스를 생성합니다. 인스턴스가 만들어지면, 모든 프로바이더에 대해 `register` 메서드를 먼저 호출합니다. 그런 다음, 모든 프로바이더가 등록된 이후에 각각의 `boot` 메서드가 실행됩니다. 이렇게 하는 이유는 `boot` 메서드가 실행될 때, 의존성 컨테이너에 필요한 바인딩이 모두 등록되어 있음을 보장하기 위해서입니다.

<!-- Essentially every major feature offered by Laravel is bootstrapped and configured by a service provider. Since they bootstrap and configure so many features offered by the framework, service providers are the most important aspect of the entire Laravel bootstrap process. -->
Laravel이 제공하는 거의 모든 주요 기능은 서비스 프로바이더를 통해 부트스트랩되고 구성됩니다. 다양한 기능의 부트스트랩과 설정을 담당하기 때문에, 서비스 프로바이더는 Laravel 부트스트랩 과정의 핵심이라고 할 수 있습니다.

<a name="routing"></a>
<!-- ### Routing -->
### Routing

<!-- One of the most important service providers in your application is the `App\Providers\RouteServiceProvider`. This service provider loads the route files contained within your application's `routes` directory. Go ahead, crack open the `RouteServiceProvider` code and take a look at how it works! -->
애플리케이션에서 가장 중요한 서비스 프로바이더 중 하나가 바로 `App\Providers\RouteServiceProvider`입니다. 이 서비스 프로바이더는 애플리케이션의 `routes` 디렉터리에 있는 라우트 파일을 불러옵니다. 기회가 된다면, 직접 `RouteServiceProvider` 코드를 열어보고 내부 동작을 살펴보시기 바랍니다!

<!-- Once the application has been bootstrapped and all service providers have been registered, the `Request` will be handed off to the router for dispatching. The router will dispatch the request to a route or controller, as well as run any route specific middleware. -->
애플리케이션이 부트스트랩되고 모든 서비스 프로바이더가 등록된 후, `Request` 객체가 라우터에 전달되어 실제 요청이 어느 라우트 또는 컨트롤러로 가야 할지 분배(dispatch)됩니다. 이 과정에서는 해당 라우트에 지정된 미들웨어들도 같이 실행됩니다.

<!-- Middleware provide a convenient mechanism for filtering or examining HTTP requests entering your application. For example, Laravel includes a middleware that verifies if the user of your application is authenticated. If the user is not authenticated, the middleware will redirect the user to the login screen. However, if the user is authenticated, the middleware will allow the request to proceed further into the application. Some middleware are assigned to all routes within the application, like those defined in the `$middleware` property of your HTTP kernel, while some are only assigned to specific routes or route groups. You can learn more about middleware by reading the complete [middleware documentation](/docs/10.x/middleware). -->
미들웨어는 애플리케이션으로 들어오는 HTTP 요청을 필터링하거나 검사할 수 있는 편리한 메커니즘을 제공합니다. 예를 들어, Laravel에는 사용자가 인증되어 있는지 확인하는 미들웨어가 포함되어 있습니다. 인증되지 않은 사용자는 로그인 화면으로 리다이렉트되고, 인증된 사용자는 애플리케이션 내부로 요청이 더 진행되도록 허용됩니다. 어떤 미들웨어는 HTTP 커널의 `$middleware` 속성에 정의되어 있어 애플리케이션의 모든 라우트에 적용되지만, 어떤 미들웨어는 특정 라우트 또는 라우트 그룹에만 할당됩니다. 미들웨어에 대한 더 자세한 내용은 전체 [middleware documentation](/docs/10.x/middleware)에서 확인하실 수 있습니다.

<!-- If the request passes through all of the matched route's assigned middleware, the route or controller method will be executed and the response returned by the route or controller method will be sent back through the route's chain of middleware. -->
요청이 라우트에 지정된 모든 미들웨어를 통과하면, 라우트 또는 컨트롤러 메서드가 실행되고, 해당 메서드가 반환한 응답이 다시 라우트의 미들웨어 체인을 통해 외부로 전달됩니다.

<a name="finishing-up"></a>
<!-- ### Finishing Up -->
### Finishing Up

<!-- Once the route or controller method returns a response, the response will travel back outward through the route's middleware, giving the application a chance to modify or examine the outgoing response. -->
라우트나 컨트롤러의 메서드가 응답을 반환하면, 이 응답은 라우트의 미들웨어를 역순으로 다시 거치면서, 애플리케이션이 최종적으로 나가는 응답을 수정하거나 검사할 수 있는 기회를 가집니다.

<!-- Finally, once the response travels back through the middleware, the HTTP kernel's `handle` method returns the response object and the `index.php` file calls the `send` method on the returned response. The `send` method sends the response content to the user's web browser. We've finished our journey through the entire Laravel request lifecycle! -->
마지막으로, 응답이 미들웨어를 모두 통과하면 HTTP 커널의 `handle` 메서드가 응답 객체를 반환하고, `index.php` 파일이 반환된 응답 객체의 `send` 메서드를 호출합니다. 이 `send` 메서드는 응답 내용을 사용자의 웹 브라우저로 전송합니다. 이제 Laravel 요청 라이프사이클의 전체 여정을 모두 마쳤습니다!

<a name="focus-on-service-providers"></a>
<!-- ## Focus on Service Providers -->
## Focus on Service Providers

<!-- Service providers are truly the key to bootstrapping a Laravel application. The application instance is created, the service providers are registered, and the request is handed to the bootstrapped application. It's really that simple! -->
서비스 프로바이더는 Laravel 애플리케이션 부트스트랩의 핵심입니다. 애플리케이션 인스턴스가 생성되고 서비스 프로바이더가 등록된 후, 요청이 이렇게 부트스트랩된 애플리케이션에 전달됩니다. 정말로 그 과정 자체는 단순합니다!

<!-- Having a firm grasp of how a Laravel application is built and bootstrapped via service providers is very valuable. Your application's default service providers are stored in the `app/Providers` directory. -->
Laravel 애플리케이션이 서비스 프로바이더를 통해 어떻게 구성되고 부트스트랩되는지 확실히 이해하는 것은 큰 도움이 됩니다. 애플리케이션의 기본 서비스 프로바이더들은 `app/Providers` 디렉터리에 저장되어 있습니다.

<!-- By default, the `AppServiceProvider` is fairly empty. This provider is a great place to add your application's own bootstrapping and service container bindings. For large applications, you may wish to create several service providers, each with more granular bootstrapping for specific services used by your application. -->
기본적으로 `AppServiceProvider`는 거의 비어있는 상태로 제공됩니다. 이 프로바이더는 애플리케이션의 고유한 부트스트랩 작업이나 서비스 컨테이너 바인딩을 추가하기에 좋은 위치입니다. 규모가 큰 애플리케이션이라면, 서비스별로 더 세분화된 부트스트랩을 위해 여러 개의 서비스 프로바이더를 만들어 관리할 수도 있습니다.
