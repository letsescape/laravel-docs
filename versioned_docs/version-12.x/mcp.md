# Laravel MCP (Laravel MCP)

- [소개](#introduction)
- [설치](#installation)
    - [라우트 게시](#publishing-routes)
- [서버 생성](#creating-servers)
    - [서버 등록](#server-registration)
    - [웹 서버](#web-servers)
    - [로컬 서버](#local-servers)
- [Tools](#tools)
    - [Tool 생성](#creating-tools)
    - [Tool 입력 스키마](#tool-input-schemas)
    - [Tool 출력 스키마](#tool-output-schemas)
    - [Tool 인수 검증](#validating-tool-arguments)
    - [Tool 의존성 주입](#tool-dependency-injection)
    - [Tool 어노테이션](#tool-annotations)
    - [조건부 Tool 등록](#conditional-tool-registration)
    - [Tool 응답](#tool-responses)
- [Prompts](#prompts)
    - [Prompt 생성](#creating-prompts)
    - [Prompt 인수](#prompt-arguments)
    - [Prompt 인수 검증](#validating-prompt-arguments)
    - [Prompt 의존성 주입](#prompt-dependency-injection)
    - [조건부 Prompt 등록](#conditional-prompt-registration)
    - [Prompt 응답](#prompt-responses)
- [Resources](#resources)
    - [Resource 생성](#creating-resources)
    - [Resource 템플릿](#resource-templates)
    - [Resource URI 및 MIME 타입](#resource-uri-and-mime-type)
    - [Resource 요청](#resource-request)
    - [Resource 의존성 주입](#resource-dependency-injection)
    - [Resource 어노테이션](#resource-annotations)
    - [조건부 Resource 등록](#conditional-resource-registration)
    - [Resource 응답](#resource-responses)
- [메타데이터](#metadata)
- [인증](#authentication)
    - [OAuth 2.1](#oauth)
    - [Sanctum](#sanctum)
- [인가](#authorization)
- [서버 테스트](#testing-servers)
    - [MCP Inspector](#mcp-inspector)
    - [Unit 테스트](#unit-tests)

<a name="introduction"></a>
## 소개

[Laravel MCP](https://github.com/laravel/mcp)는 AI 클라이언트가 [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro)을 통해 Laravel 애플리케이션과 상호작용할 수 있도록 하는 간단하고 우아한 방법을 제공합니다.  

이 패키지는 서버, tools, resources, prompts를 정의할 수 있는 표현력 있고 유연한 인터페이스를 제공하여 AI 기반 상호작용을 애플리케이션에 쉽게 통합할 수 있도록 합니다.

<a name="installation"></a>
## 설치

Composer 패키지 매니저를 사용하여 Laravel MCP를 프로젝트에 설치합니다.

```shell
composer require laravel/mcp
```

<a name="publishing-routes"></a>
### 라우트 게시

Laravel MCP를 설치한 후 `vendor:publish` Artisan 명령어를 실행하여 MCP 서버를 정의할 `routes/ai.php` 파일을 게시합니다.

```shell
php artisan vendor:publish --tag=ai-routes
```

이 명령어는 애플리케이션의 `routes` 디렉토리에 `routes/ai.php` 파일을 생성하며, 이 파일에서 MCP 서버를 등록하게 됩니다.

<a name="creating-servers"></a>
## 서버 생성

`make:mcp-server` Artisan 명령어를 사용하여 MCP 서버를 생성할 수 있습니다. 서버는 AI 클라이언트에 tools, resources, prompts 같은 MCP 기능을 노출하는 중앙 통신 지점 역할을 합니다.

```shell
php artisan make:mcp-server WeatherServer
```

이 명령어는 `app/Mcp/Servers` 디렉토리에 새로운 서버 클래스를 생성합니다.  
생성된 서버 클래스는 Laravel MCP의 기본 `Laravel\Mcp\Server` 클래스를 확장하며 서버 설정과 tool, resource, prompt 등록을 위한 속성과 프로퍼티를 제공합니다.

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

서버를 생성한 후에는 `routes/ai.php` 파일에 등록해야 실제로 사용할 수 있습니다.  

Laravel MCP는 두 가지 방식의 서버 등록 방법을 제공합니다.

- `web` : HTTP 요청으로 접근하는 서버
- `local` : 커맨드라인에서 실행되는 서버

<a name="web-servers"></a>
### 웹 서버

웹 서버는 가장 일반적인 형태의 MCP 서버입니다. HTTP POST 요청을 통해 접근할 수 있으므로 원격 AI 클라이언트나 웹 기반 통합에 적합합니다.

```php
use App\Mcp\Servers\WeatherServer;
use Laravel\Mcp\Facades\Mcp;

Mcp::web('/mcp/weather', WeatherServer::class);
```

일반 라우트와 동일하게 미들웨어를 적용하여 보호할 수도 있습니다.

```php
Mcp::web('/mcp/weather', WeatherServer::class)
    ->middleware(['throttle:mcp']);
```

<a name="local-servers"></a>
### 로컬 서버

로컬 서버는 Artisan 명령어로 실행되는 서버입니다.  

예를 들어 [Laravel Boost](/docs/12.x/installation#installing-laravel-boost) 같은 로컬 AI 어시스턴트 통합을 만들 때 유용합니다.

```php
use App\Mcp\Servers\WeatherServer;
use Laravel\Mcp\Facades\Mcp;

Mcp::local('weather', WeatherServer::class);
```

등록이 완료되면 일반적으로 `mcp:start` Artisan 명령어를 직접 실행할 필요는 없습니다. 대신 MCP 클라이언트(AI 에이전트)가 서버를 시작하도록 설정하거나 [MCP Inspector](#mcp-inspector)를 사용할 수 있습니다.

---

## Tools

Tools는 서버가 AI 클라이언트에 기능을 노출하도록 합니다.  

언어 모델이 특정 작업을 수행하거나 코드 실행, 외부 시스템과의 상호작용 등을 할 수 있도록 하는 기능입니다.

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

<a name="creating-tools"></a>
### Tool 생성

Tool을 생성하려면 `make:mcp-tool` Artisan 명령어를 실행합니다.

```shell
php artisan make:mcp-tool CurrentWeatherTool
```

생성한 Tool은 서버의 `$tools` 프로퍼티에 등록해야 합니다.

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

<a name="tool-name-title-description"></a>
#### Tool Name, Title, Description

기본적으로 Tool의 name과 title은 클래스 이름에서 자동 생성됩니다.

예:  
`CurrentWeatherTool`  
- name: `current-weather`  
- title: `Current Weather Tool`

이 값은 `Name`, `Title` 속성(attribute)을 사용하여 커스터마이즈할 수 있습니다.

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

Tool의 설명은 자동으로 생성되지 않기 때문에 `Description` 속성을 사용하여 반드시 의미 있는 설명을 작성해야 합니다.

```php
use Laravel\Mcp\Server\Attributes\Description;

#[Description('Fetches the current weather forecast for a specified location.')]
class CurrentWeatherTool extends Tool
{
    //
}
```

> [!NOTE]
> 설명(description)은 Tool 메타데이터에서 매우 중요한 요소입니다.  
> AI 모델이 언제, 어떤 방식으로 Tool을 사용해야 하는지 이해하는 데 핵심적인 역할을 합니다.

---

(문서가 매우 길어 메시지 제한에 걸려 **이후 섹션은 다음 메시지에서 이어서 번역**됩니다.)