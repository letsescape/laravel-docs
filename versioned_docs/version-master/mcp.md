# Laravel MCP

- [소개](#introduction)
- [설치](#installation)
    - [라우트 게시](#publishing-routes)
- [서버 생성](#creating-servers)
    - [서버 등록](#server-registration)
    - [웹 서버](#web-servers)
    - [로컬 서버](#local-servers)
- [도구](#tools)
    - [도구 생성](#creating-tools)
    - [도구 입력 스키마](#tool-input-schemas)
    - [도구 출력 스키마](#tool-output-schemas)
    - [도구 인수 유효성 검증](#validating-tool-arguments)
    - [도구 의존성 주입](#tool-dependency-injection)
    - [도구 애너테이션](#tool-annotations)
    - [조건부 도구 등록](#conditional-tool-registration)
    - [도구 응답](#tool-responses)
- [프롬프트](#prompts)
    - [프롬프트 생성](#creating-prompts)
    - [프롬프트 인수](#prompt-arguments)
    - [프롬프트 인수 유효성 검증](#validating-prompt-arguments)
    - [프롬프트 의존성 주입](#prompt-dependency-injection)
    - [조건부 프롬프트 등록](#conditional-prompt-registration)
    - [프롬프트 응답](#prompt-responses)
- [리소스](#resources)
    - [리소스 생성](#creating-resources)
    - [리소스 템플릿](#resource-templates)
    - [리소스 URI 및 MIME 타입](#resource-uri-and-mime-type)
    - [리소스 요청](#resource-request)
    - [리소스 의존성 주입](#resource-dependency-injection)
    - [리소스 애너테이션](#resource-annotations)
    - [조건부 리소스 등록](#conditional-resource-registration)
    - [리소스 응답](#resource-responses)
- [메타데이터](#metadata)
- [인증](#authentication)
    - [OAuth 2.1](#oauth)
    - [Sanctum](#sanctum)
- [인가](#authorization)
- [서버 테스트](#testing-servers)
    - [MCP Inspector](#mcp-inspector)
    - [단위 테스트](#unit-tests)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel MCP](https://github.com/laravel/mcp)는 AI 클라이언트가 [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro)을 통해 Laravel 애플리케이션과 상호작용할 수 있도록 간단하고 우아한 방법을 제공합니다.  

서버, 도구(tools), 리소스(resources), 프롬프트(prompts)를 정의할 수 있는 표현력 있는 fluent 인터페이스를 제공하여 AI 기반 상호작용을 애플리케이션에 쉽게 통합할 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

시작하려면 Composer 패키지 매니저를 사용하여 Laravel MCP를 프로젝트에 설치합니다.

```shell
composer require laravel/mcp
```

<a name="publishing-routes"></a>
### 라우트 게시

Laravel MCP 설치 후 `vendor:publish` Artisan 명령어를 실행하여 MCP 서버를 정의할 `routes/ai.php` 파일을 게시합니다.

```shell
php artisan vendor:publish --tag=ai-routes
```

이 명령어는 애플리케이션의 `routes` 디렉터리에 `routes/ai.php` 파일을 생성하며, 이 파일에서 MCP 서버를 등록하게 됩니다.

<a name="creating-servers"></a>
## 서버 생성 (Creating Servers)

`make:mcp-server` Artisan 명령어를 사용하여 MCP 서버를 생성할 수 있습니다.  

서버는 AI 클라이언트에 tools, resources, prompts와 같은 MCP 기능을 노출하는 중앙 통신 지점 역할을 합니다.

```shell
php artisan make:mcp-server WeatherServer
```

이 명령어를 실행하면 `app/Mcp/Servers` 디렉터리에 새로운 서버 클래스가 생성됩니다.  

생성된 클래스는 Laravel MCP의 기본 `Laravel\Mcp\Server` 클래스를 상속하며, 서버 설정과 tools, resources, prompts 등록을 위한 속성과 프로퍼티를 제공합니다.

```php
<?php

namespace App\Mcp\Servers;

use Laravel\Mcp\Server\Attributes\Instructions;
use Laravel\Mcp\Server\Attributes\Name;
use Laravel\Mcp\Server\Attributes\Version;
use Laravel\Mcp\Server;

#[Name('Weather Server')]
#[Version('1.0.0')]
#[Instructions('This server provides weather information and forecasts.')]
class WeatherServer extends Server
{
    /**
     * The tools registered with this MCP server.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Tool>>
     */
    protected array $tools = [
        // GetCurrentWeatherTool::class,
    ];

    /**
     * The resources registered with this MCP server.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Resource>>
     */
    protected array $resources = [
        // WeatherGuidelinesResource::class,
    ];

    /**
     * The prompts registered with this MCP server.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Prompt>>
     */
    protected array $prompts = [
        // DescribeWeatherPrompt::class,
    ];
}
```

<a name="server-registration"></a>
### 서버 등록

서버를 생성한 후에는 `routes/ai.php` 파일에 등록해야 실제로 접근할 수 있습니다.  

Laravel MCP는 서버 등록을 위해 두 가지 방법을 제공합니다.

- `web` : HTTP로 접근 가능한 서버
- `local` : CLI 기반 서버

<a name="web-servers"></a>
### 웹 서버

웹 서버는 가장 일반적인 형태이며 HTTP POST 요청을 통해 접근합니다.  
원격 AI 클라이언트나 웹 기반 통합에 적합합니다.

```php
use App\Mcp\Servers\WeatherServer;
use Laravel\Mcp\Facades\Mcp;

Mcp::web('/mcp/weather', WeatherServer::class);
```

일반 라우트처럼 middleware를 적용하여 서버를 보호할 수도 있습니다.

```php
Mcp::web('/mcp/weather', WeatherServer::class)
    ->middleware(['throttle:mcp']);
```

<a name="local-servers"></a>
### 로컬 서버

로컬 서버는 Artisan 명령어로 실행되는 서버입니다.  

[Laravel Boost](/docs/master/installation#installing-laravel-boost)와 같은 로컬 AI 어시스턴트 통합을 구축할 때 유용합니다.

```php
use App\Mcp\Servers\WeatherServer;
use Laravel\Mcp\Facades\Mcp;

Mcp::local('weather', WeatherServer::class);
```

서버가 등록되면 일반적으로 `mcp:start` Artisan 명령어를 직접 실행할 필요는 없습니다.  

대신 MCP 클라이언트(AI 에이전트)가 서버를 시작하도록 설정하거나 [MCP Inspector](#mcp-inspector)를 사용할 수 있습니다.

<a name="tools"></a>
## 도구 (Tools)

도구는 서버가 AI 클라이언트에 기능을 제공할 수 있도록 합니다.  

언어 모델이 작업을 수행하거나 코드를 실행하거나 외부 시스템과 상호작용할 수 있게 합니다.

```php
<?php

namespace App\Mcp\Tools;

use Illuminate\Contracts\JsonSchema\JsonSchema;
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Attributes\Description;
use Laravel\Mcp\Server\Tool;

#[Description('Fetches the current weather forecast for a specified location.')]
class CurrentWeatherTool extends Tool
{
    /**
     * Handle the tool request.
     */
    public function handle(Request $request): Response
    {
        $location = $request->get('location');

        // Get weather...

        return Response::text('The weather is...');
    }

    /**
     * Get the tool's input schema.
     *
     * @return array<string, \Illuminate\JsonSchema\Types\Type>
     */
    public function schema(JsonSchema $schema): array
    {
        return [
            'location' => $schema->string()
                ->description('The location to get the weather for.')
                ->required(),
        ];
    }
}
```

### 도구 생성

도구를 생성하려면 다음 Artisan 명령어를 실행합니다.

```shell
php artisan make:mcp-tool CurrentWeatherTool
```

도구를 생성한 후 서버의 `$tools` 프로퍼티에 등록해야 합니다.

```php
<?php

namespace App\Mcp\Servers;

use App\Mcp\Tools\CurrentWeatherTool;
use Laravel\Mcp\Server;

class WeatherServer extends Server
{
    /**
     * The tools registered with this MCP server.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Tool>>
     */
    protected array $tools = [
        CurrentWeatherTool::class,
    ];
}
```

#### 도구 이름, 제목, 설명

기본적으로 도구의 name과 title은 클래스 이름에서 자동 생성됩니다.  

예를 들어 `CurrentWeatherTool` 클래스는 다음과 같이 변환됩니다.

- name : `current-weather`
- title : `Current Weather Tool`

이 값들은 `Name`과 `Title` attribute로 변경할 수 있습니다.

```php
use Laravel\Mcp\Server\Attributes\Name;
use Laravel\Mcp\Server\Attributes\Title;

#[Name('get-optimistic-weather')]
#[Title('Get Optimistic Weather Forecast')]
class CurrentWeatherTool extends Tool
{
    // ...
}
```

도구 설명은 자동 생성되지 않기 때문에 반드시 `Description` attribute로 명시해야 합니다.

```php
use Laravel\Mcp\Server\Attributes\Description;

#[Description('Fetches the current weather forecast for a specified location.')]
class CurrentWeatherTool extends Tool
{
    //
}
```

> [!NOTE]
> description은 도구 메타데이터의 매우 중요한 요소입니다. AI 모델이 언제, 어떻게 이 도구를 사용해야 하는지 이해하는 데 도움이 됩니다.

(문서가 매우 길어 메시지 제한에 도달했기 때문에 이후 섹션은 다음 응답에서 계속됩니다.)