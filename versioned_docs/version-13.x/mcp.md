# Laravel MCP (Laravel MCP)

- [소개](#introduction)
- [설치](#installation)
    - [라우트 퍼블리싱](#publishing-routes)
- [서버 생성](#creating-servers)
    - [서버 등록](#server-registration)
    - [웹 서버](#web-servers)
    - [로컬 서버](#local-servers)
- [도구 (Tools)](#tools)
    - [Tool 생성](#creating-tools)
    - [Tool 입력 스키마](#tool-input-schemas)
    - [Tool 출력 스키마](#tool-output-schemas)
    - [Tool 인수 유효성 검사](#validating-tool-arguments)
    - [Tool 의존성 주입](#tool-dependency-injection)
    - [Tool 어노테이션](#tool-annotations)
    - [조건부 Tool 등록](#conditional-tool-registration)
    - [Tool 응답](#tool-responses)
- [프롬프트 (Prompts)](#prompts)
    - [Prompt 생성](#creating-prompts)
    - [Prompt 인수](#prompt-arguments)
    - [Prompt 인수 유효성 검사](#validating-prompt-arguments)
    - [Prompt 의존성 주입](#prompt-dependency-injection)
    - [조건부 Prompt 등록](#conditional-prompt-registration)
    - [Prompt 응답](#prompt-responses)
- [리소스 (Resources)](#resources)
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
    - [유닛 테스트](#unit-tests)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel MCP](https://github.com/laravel/mcp)는 AI 클라이언트가 [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro)을 통해 Laravel 애플리케이션과 상호작용할 수 있도록 하는 간단하고 우아한 방법을 제공합니다. 서버, Tool, Resource, Prompt를 정의할 수 있는 표현력 있고 유연한 인터페이스를 제공하여 AI 기반 상호작용을 애플리케이션에 쉽게 통합할 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

시작하려면 Composer 패키지 매니저를 사용하여 Laravel MCP를 프로젝트에 설치합니다.

```shell
composer require laravel/mcp
```

<a name="publishing-routes"></a>
### 라우트 퍼블리싱

Laravel MCP를 설치한 후 `vendor:publish` Artisan 명령어를 실행하여 MCP 서버를 정의할 `routes/ai.php` 파일을 퍼블리싱합니다.

```shell
php artisan vendor:publish --tag=ai-routes
```

이 명령어는 애플리케이션의 `routes` 디렉토리에 `routes/ai.php` 파일을 생성하며, 이 파일을 사용하여 MCP 서버를 등록하게 됩니다.

<a name="creating-servers"></a>
## 서버 생성 (Creating Servers)

`make:mcp-server` Artisan 명령어를 사용하여 MCP 서버를 생성할 수 있습니다. 서버는 Tool, Resource, Prompt와 같은 MCP 기능을 AI 클라이언트에 노출하는 중앙 통신 지점 역할을 합니다.

```shell
php artisan make:mcp-server WeatherServer
```

이 명령어는 `app/Mcp/Servers` 디렉토리에 새로운 서버 클래스를 생성합니다. 생성된 서버 클래스는 Laravel MCP의 기본 `Laravel\Mcp\Server` 클래스를 확장하며, 서버 설정과 Tool, Resource, Prompt 등록을 위한 속성과 프로퍼티를 제공합니다.

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

서버를 생성한 후에는 `routes/ai.php` 파일에 등록하여 접근 가능하게 만들어야 합니다. Laravel MCP는 서버를 등록하는 두 가지 메서드를 제공합니다. HTTP로 접근 가능한 서버를 위한 `web` 메서드와 커맨드라인 서버를 위한 `local` 메서드입니다.

<a name="web-servers"></a>
### 웹 서버

웹 서버는 가장 일반적인 유형의 서버로, HTTP POST 요청을 통해 접근할 수 있어 원격 AI 클라이언트나 웹 기반 통합에 적합합니다. `web` 메서드를 사용하여 웹 서버를 등록합니다.

```php
use App\Mcp\Servers\WeatherServer;
use Laravel\Mcp\Facades\Mcp;

Mcp::web('/mcp/weather', WeatherServer::class);
```

일반 라우트와 마찬가지로, 웹 서버에 미들웨어를 적용하여 보호할 수 있습니다.

```php
Mcp::web('/mcp/weather', WeatherServer::class)
    ->middleware(['throttle:mcp']);
```

<a name="local-servers"></a>
### 로컬 서버

로컬 서버는 Artisan 명령어로 실행되며, [Laravel Boost](/docs/13.x/installation#installing-laravel-boost)와 같은 로컬 AI 어시스턴트 통합을 구축하는 데 적합합니다. `local` 메서드를 사용하여 로컬 서버를 등록합니다.

```php
use App\Mcp\Servers\WeatherServer;
use Laravel\Mcp\Facades\Mcp;

Mcp::local('weather', WeatherServer::class);
```

등록이 완료되면, 일반적으로 `mcp:start` Artisan 명령어를 직접 실행할 필요는 없습니다. 대신 MCP 클라이언트(AI 에이전트)가 서버를 시작하도록 설정하거나 [MCP Inspector](#mcp-inspector)를 사용하세요.

<a name="tools"></a>
## 도구 (Tools)

Tool은 서버가 AI 클라이언트가 호출할 수 있는 기능을 노출할 수 있게 해줍니다. 언어 모델이 작업을 수행하거나, 코드를 실행하거나, 외부 시스템과 상호작용할 수 있도록 합니다.

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

Tool을 생성한 후에는 서버의 `$tools` 프로퍼티에 등록합니다.

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
#### Tool 이름, 제목, 설명

기본적으로 Tool의 이름과 제목은 클래스 이름에서 자동으로 생성됩니다. 예를 들어, `CurrentWeatherTool`은 이름이 `current-weather`이고 제목이 `Current Weather Tool`이 됩니다. `Name` 및 `Title` 속성을 사용하여 이 값을 사용자 지정할 수 있습니다.

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

Tool 설명은 자동으로 생성되지 않습니다. `Description` 속성을 사용하여 항상 의미 있는 설명을 제공해야 합니다.

```php
use Laravel\Mcp\Server\Attributes\Description;

#[Description('Fetches the current weather forecast for a specified location.')]
class CurrentWeatherTool extends Tool
{
    //
}
```

> [!NOTE]
> 설명은 Tool 메타데이터에서 매우 중요한 부분으로, AI 모델이 Tool을 언제 그리고 어떻게 효과적으로 사용해야 하는지 이해하는 데 도움을 줍니다.

<a name="tool-input-schemas"></a>
### Tool 입력 스키마

Tool은 AI 클라이언트로부터 어떤 인수를 받을지 지정하는 입력 스키마를 정의할 수 있습니다. Laravel의 `Illuminate\Contracts\JsonSchema\JsonSchema` 빌더를 사용하여 Tool의 입력 요구사항을 정의합니다.

```php
<?php

namespace App\Mcp\Tools;

use Illuminate\Contracts\JsonSchema\JsonSchema;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
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

            'units' => $schema->string()
                ->enum(['celsius', 'fahrenheit'])
                ->description('The temperature units to use.')
                ->default('celsius'),
        ];
    }
}
```

<a name="tool-output-schemas"></a>
### Tool 출력 스키마

Tool은 응답의 구조를 지정하는 [출력 스키마](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#output-schema)를 정의할 수 있습니다. 이를 통해 파싱 가능한 Tool 결과가 필요한 AI 클라이언트와의 더 나은 통합이 가능합니다. `outputSchema` 메서드를 사용하여 Tool의 출력 구조를 정의합니다.

```php
<?php

namespace App\Mcp\Tools;

use Illuminate\Contracts\JsonSchema\JsonSchema;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * Get the tool's output schema.
     *
     * @return array<string, \Illuminate\JsonSchema\Types\Type>
     */
    public function outputSchema(JsonSchema $schema): array
    {
        return [
            'temperature' => $schema->number()
                ->description('Temperature in Celsius')
                ->required(),

            'conditions' => $schema->string()
                ->description('Weather conditions')
                ->required(),

            'humidity' => $schema->integer()
                ->description('Humidity percentage')
                ->required(),
        ];
    }
}
```

<a name="validating-tool-arguments"></a>
### Tool 인수 유효성 검사

JSON Schema 정의는 Tool 인수에 대한 기본적인 구조를 제공하지만, 더 복잡한 유효성 검사 규칙을 적용하고 싶을 수도 있습니다.

Laravel MCP는 Laravel의 [유효성 검사 기능](/docs/13.x/validation)과 원활하게 통합됩니다. Tool의 `handle` 메서드 내에서 들어오는 Tool 인수를 유효성 검사할 수 있습니다.

```php
<?php

namespace App\Mcp\Tools;

use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * Handle the tool request.
     */
    public function handle(Request $request): Response
    {
        $validated = $request->validate([
            'location' => 'required|string|max:100',
            'units' => 'in:celsius,fahrenheit',
        ]);

        // Fetch weather data using the validated arguments...
    }
}
```

유효성 검사 실패 시, AI 클라이언트는 제공된 오류 메시지를 기반으로 동작합니다. 따라서 명확하고 실행 가능한 오류 메시지를 제공하는 것이 중요합니다.

```php
$validated = $request->validate([
    'location' => ['required','string','max:100'],
    'units' => 'in:celsius,fahrenheit',
],[
    'location.required' => 'You must specify a location to get the weather for. For example, "New York City" or "Tokyo".',
    'units.in' => 'You must specify either "celsius" or "fahrenheit" for the units.',
]);
```

<a name="tool-dependency-injection"></a>
#### Tool 의존성 주입

모든 Tool은 Laravel [서비스 컨테이너](/docs/13.x/container)를 통해 리졸브됩니다. 따라서 Tool의 생성자에서 필요한 의존성을 타입 힌트로 지정할 수 있습니다. 선언된 의존성은 자동으로 리졸브되어 Tool 인스턴스에 주입됩니다.

```php
<?php

namespace App\Mcp\Tools;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * Create a new tool instance.
     */
    public function __construct(
        protected WeatherRepository $weather,
    ) {}

    // ...
}
```

생성자 주입 외에도 Tool의 `handle()` 메서드에서 의존성을 타입 힌트로 지정할 수 있습니다. 서비스 컨테이너는 메서드가 호출될 때 자동으로 의존성을 리졸브하고 주입합니다.

```php
<?php

namespace App\Mcp\Tools;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * Handle the tool request.
     */
    public function handle(Request $request, WeatherRepository $weather): Response
    {
        $location = $request->get('location');

        $forecast = $weather->getForecastFor($location);

        // ...
    }
}
```

<a name="tool-annotations"></a>
### Tool 어노테이션

[어노테이션](https://modelcontextprotocol.io/specification/2025-06-18/schema#toolannotations)을 사용하여 AI 클라이언트에 추가 메타데이터를 제공함으로써 Tool을 향상시킬 수 있습니다. 이러한 어노테이션은 AI 모델이 Tool의 동작과 기능을 이해하는 데 도움을 줍니다. 어노테이션은 속성(attribute)을 통해 Tool에 추가됩니다.

```php
<?php

namespace App\Mcp\Tools;

use Laravel\Mcp\Server\Tools\Annotations\IsIdempotent;
use Laravel\Mcp\Server\Tools\Annotations\IsReadOnly;
use Laravel\Mcp\Server\Tool;

#[IsIdempotent]
#[IsReadOnly]
class CurrentWeatherTool extends Tool
{
    //
}
```

사용 가능한 어노테이션은 다음과 같습니다.

| 어노테이션 | 타입 | 설명 |
| --- | --- | --- |
| `#[IsReadOnly]` | boolean | Tool이 환경을 수정하지 않음을 나타냅니다. |
| `#[IsDestructive]` | boolean | Tool이 파괴적인 업데이트를 수행할 수 있음을 나타냅니다(읽기 전용이 아닌 경우에만 의미 있음). |
| `#[IsIdempotent]` | boolean | 동일한 인수로 반복 호출해도 추가 효과가 없음을 나타냅니다(읽기 전용이 아닌 경우). |
| `#[IsOpenWorld]` | boolean | Tool이 외부 엔티티와 상호작용할 수 있음을 나타냅니다. |

어노테이션 값은 boolean 인수를 사용하여 명시적으로 설정할 수 있습니다.

```php
use Laravel\Mcp\Server\Tools\Annotations\IsReadOnly;
use Laravel\Mcp\Server\Tools\Annotations\IsDestructive;
use Laravel\Mcp\Server\Tools\Annotations\IsOpenWorld;
use Laravel\Mcp\Server\Tools\Annotations\IsIdempotent;
use Laravel\Mcp\Server\Tool;

#[IsReadOnly(true)]
#[IsDestructive(false)]
#[IsOpenWorld(false)]
#[IsIdempotent(true)]
class CurrentWeatherTool extends Tool
{
    //
}
```

<a name="conditional-tool-registration"></a>
### 조건부 Tool 등록

Tool 클래스에 `shouldRegister` 메서드를 구현하여 런타임에 조건부로 Tool을 등록할 수 있습니다. 이 메서드를 사용하면 애플리케이션 상태, 설정 또는 요청 파라미터에 따라 Tool의 사용 가능 여부를 결정할 수 있습니다.

```php
<?php

namespace App\Mcp\Tools;

use Laravel\Mcp\Request;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * Determine if the tool should be registered.
     */
    public function shouldRegister(Request $request): bool
    {
        return $request?->user()?->subscribed() ?? false;
    }
}
```

Tool의 `shouldRegister` 메서드가 `false`를 반환하면, 사용 가능한 Tool 목록에 표시되지 않으며 AI 클라이언트가 호출할 수 없습니다.

<a name="tool-responses"></a>
### Tool 응답

Tool은 반드시 `Laravel\Mcp\Response` 인스턴스를 반환해야 합니다. Response 클래스는 다양한 유형의 응답을 생성하기 위한 여러 편리한 메서드를 제공합니다.

단순 텍스트 응답의 경우 `text` 메서드를 사용합니다.

```php
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;

/**
 * Handle the tool request.
 */
public function handle(Request $request): Response
{
    // ...

    return Response::text('Weather Summary: Sunny, 72°F');
}
```

Tool 실행 중 오류가 발생했음을 나타내려면 `error` 메서드를 사용합니다.

```php
return Response::error('Unable to fetch weather data. Please try again.');
```

이미지 또는 오디오 콘텐츠를 반환하려면 `image` 및 `audio` 메서드를 사용합니다.

```php
return Response::image(file_get_contents(storage_path('weather/radar.png')), 'image/png');

return Response::audio(file_get_contents(storage_path('weather/alert.mp3')), 'audio/mp3');
```

`fromStorage` 메서드를 사용하여 Laravel 파일시스템 디스크에서 직접 이미지 및 오디오 콘텐츠를 로드할 수도 있습니다. MIME 타입은 파일에서 자동으로 감지됩니다.

```php
return Response::fromStorage('weather/radar.png');
```

필요한 경우 특정 디스크를 지정하거나 MIME 타입을 오버라이드할 수 있습니다.

```php
return Response::fromStorage('weather/radar.png', disk: 's3');

return Response::fromStorage('weather/radar.png', mimeType: 'image/webp');
```

<a name="multiple-content-responses"></a>
#### 다중 콘텐츠 응답

Tool은 `Response` 인스턴스의 배열을 반환하여 여러 개의 콘텐츠를 반환할 수 있습니다.

```php
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;

/**
 * Handle the tool request.
 *
 * @return array<int, \Laravel\Mcp\Response>
 */
public function handle(Request $request): array
{
    // ...

    return [
        Response::text('Weather Summary: Sunny, 72°F'),
        Response::text('**Detailed Forecast**\n- Morning: 65°F\n- Afternoon: 78°F\n- Evening: 70°F')
    ];
}
```

<a name="structured-responses"></a>
#### 구조화된 응답

Tool은 `structured` 메서드를 사용하여 [구조화된 콘텐츠](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#structured-content)를 반환할 수 있습니다. 이는 JSON으로 인코딩된 텍스트 표현과의 하위 호환성을 유지하면서 AI 클라이언트에게 파싱 가능한 데이터를 제공합니다.

```php
return Response::structured([
    'temperature' => 22.5,
    'conditions' => 'Partly cloudy',
    'humidity' => 65,
]);
```

구조화된 콘텐츠와 함께 사용자 정의 텍스트를 제공해야 하는 경우 Response 팩토리의 `withStructuredContent` 메서드를 사용합니다.

```php
return Response::make(
    Response::text('Weather is 22.5°C and sunny')
)->withStructuredContent([
    'temperature' => 22.5,
    'conditions' => 'Sunny',
]);
```

<a name="streaming-responses"></a>
#### 스트리밍 응답

장시간 실행되는 작업이나 실시간 데이터 스트리밍의 경우, Tool은 `handle` 메서드에서 [제너레이터](https://www.php.net/manual/en/language.generators.overview.php)를 반환할 수 있습니다. 이를 통해 최종 응답 전에 클라이언트에 중간 업데이트를 보낼 수 있습니다.

```php
<?php

namespace App\Mcp\Tools;

use Generator;
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * Handle the tool request.
     *
     * @return \Generator<int, \Laravel\Mcp\Response>
     */
    public function handle(Request $request): Generator
    {
        $locations = $request->array('locations');

        foreach ($locations as $index => $location) {
            yield Response::notification('processing/progress', [
                'current' => $index + 1,
                'total' => count($locations),
                'location' => $location,
            ]);

            yield Response::text($this->forecastFor($location));
        }
    }
}
```

웹 기반 서버를 사용할 때, 스트리밍 응답은 자동으로 SSE(Server-Sent Events) 스트림을 열어 yield된 각 메시지를 이벤트로 클라이언트에 전송합니다.

<a name="prompts"></a>
## 프롬프트 (Prompts)

[Prompts](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts)는 서버가 AI 클라이언트가 언어 모델과 상호작용하는 데 사용할 수 있는 재사용 가능한 프롬프트 템플릿을 공유할 수 있게 해줍니다. 일반적인 쿼리와 상호작용을 구조화하는 표준화된 방법을 제공합니다.

<a name="creating-prompts"></a>
### Prompt 생성

Prompt를 생성하려면 `make:mcp-prompt` Artisan 명령어를 실행합니다.

```shell
php artisan make:mcp-prompt DescribeWeatherPrompt
```

Prompt를 생성한 후에는 서버의 `$prompts` 프로퍼티에 등록합니다.

```php
<?php

namespace App\Mcp\Servers;

use App\Mcp\Prompts\DescribeWeatherPrompt;
use Laravel\Mcp\Server;

class WeatherServer extends Server
{
    /**
     * The prompts registered with this MCP server.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Prompt>>
     */
    protected array $prompts = [
        DescribeWeatherPrompt::class,
    ];
}
```

<a name="prompt-name-title-and-description"></a>
#### Prompt 이름, 제목, 설명

기본적으로 Prompt의 이름과 제목은 클래스 이름에서 자동으로 생성됩니다. 예를 들어, `DescribeWeatherPrompt`는 이름이 `describe-weather`이고 제목이 `Describe Weather Prompt`가 됩니다. `Name` 및 `Title` 속성을 사용하여 이 값을 사용자 지정할 수 있습니다.

```php
use Laravel\Mcp\Server\Attributes\Name;
use Laravel\Mcp\Server\Attributes\Title;

#[Name('weather-assistant')]
#[Title('Weather Assistant Prompt')]
class DescribeWeatherPrompt extends Prompt
{
    // ...
}
```

Prompt 설명은 자동으로 생성되지 않습니다. `Description` 속성을 사용하여 항상 의미 있는 설명을 제공해야 합니다.

```php
use Laravel\Mcp\Server\Attributes\Description;

#[Description('Generates a natural-language explanation of the weather for a given location.')]
class DescribeWeatherPrompt extends Prompt
{
    //
}
```

> [!NOTE]
> 설명은 Prompt 메타데이터에서 매우 중요한 부분으로, AI 모델이 Prompt를 언제 그리고 어떻게 최대한 활용해야 하는지 이해하는 데 도움을 줍니다.

<a name="prompt-arguments"></a>
### Prompt 인수

Prompt는 AI 클라이언트가 프롬프트 템플릿을 특정 값으로 사용자 지정할 수 있도록 인수를 정의할 수 있습니다. `arguments` 메서드를 사용하여 Prompt가 받는 인수를 정의합니다.

```php
<?php

namespace App\Mcp\Prompts;

use Laravel\Mcp\Server\Prompt;
use Laravel\Mcp\Server\Prompts\Argument;

class DescribeWeatherPrompt extends Prompt
{
    /**
     * Get the prompt's arguments.
     *
     * @return array<int, \Laravel\Mcp\Server\Prompts\Argument>
     */
    public function arguments(): array
    {
        return [
            new Argument(
                name: 'tone',
                description: 'The tone to use in the weather description (e.g., formal, casual, humorous).',
                required: true,
            ),
        ];
    }
}
```

<a name="validating-prompt-arguments"></a>
### Prompt 인수 유효성 검사

Prompt 인수는 정의에 따라 자동으로 유효성 검사가 이루어지지만, 더 복잡한 유효성 검사 규칙을 적용하고 싶을 수도 있습니다.

Laravel MCP는 Laravel의 [유효성 검사 기능](/docs/13.x/validation)과 원활하게 통합됩니다. Prompt의 `handle` 메서드 내에서 들어오는 Prompt 인수를 유효성 검사할 수 있습니다.

```php
<?php

namespace App\Mcp\Prompts;

use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Prompt;

class DescribeWeatherPrompt extends Prompt
{
    /**
     * Handle the prompt request.
     */
    public function handle(Request $request): Response
    {
        $validated = $request->validate([
            'tone' => 'required|string|max:50',
        ]);

        $tone = $validated['tone'];

        // Generate the prompt response using the given tone...
    }
}
```

유효성 검사 실패 시, AI 클라이언트는 제공된 오류 메시지를 기반으로 동작합니다. 따라서 명확하고 실행 가능한 오류 메시지를 제공하는 것이 중요합니다.

```php
$validated = $request->validate([
    'tone' => ['required','string','max:50'],
],[
    'tone.*' => 'You must specify a tone for the weather description. Examples include "formal", "casual", or "humorous".',
]);
```

<a name="prompt-dependency-injection"></a>
### Prompt 의존성 주입

모든 Prompt는 Laravel [서비스 컨테이너](/docs/13.x/container)를 통해 리졸브됩니다. 따라서 Prompt의 생성자에서 필요한 의존성을 타입 힌트로 지정할 수 있습니다. 선언된 의존성은 자동으로 리졸브되어 Prompt 인스턴스에 주입됩니다.

```php
<?php

namespace App\Mcp\Prompts;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Server\Prompt;

class DescribeWeatherPrompt extends Prompt
{
    /**
     * Create a new prompt instance.
     */
    public function __construct(
        protected WeatherRepository $weather,
    ) {}

    //
}
```

생성자 주입 외에도 Prompt의 `handle` 메서드에서 의존성을 타입 힌트로 지정할 수 있습니다. 서비스 컨테이너는 메서드가 호출될 때 자동으로 의존성을 리졸브하고 주입합니다.

```php
<?php

namespace App\Mcp\Prompts;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Prompt;

class DescribeWeatherPrompt extends Prompt
{
    /**
     * Handle the prompt request.
     */
    public function handle(Request $request, WeatherRepository $weather): Response
    {
        $isAvailable = $weather->isServiceAvailable();

        // ...
    }
}
```

<a name="conditional-prompt-registration"></a>
### 조건부 Prompt 등록

Prompt 클래스에 `shouldRegister` 메서드를 구현하여 런타임에 조건부로 Prompt를 등록할 수 있습니다. 이 메서드를 사용하면 애플리케이션 상태, 설정 또는 요청 파라미터에 따라 Prompt의 사용 가능 여부를 결정할 수 있습니다.

```php
<?php

namespace App\Mcp\Prompts;

use Laravel\Mcp\Request;
use Laravel\Mcp\Server\Prompt;

class CurrentWeatherPrompt extends Prompt
{
    /**
     * Determine if the prompt should be registered.
     */
    public function shouldRegister(Request $request): bool
    {
        return $request?->user()?->subscribed() ?? false;
    }
}
```

Prompt의 `shouldRegister` 메서드가 `false`를 반환하면, 사용 가능한 Prompt 목록에 표시되지 않으며 AI 클라이언트가 호출할 수 없습니다.

<a name="prompt-responses"></a>
### Prompt 응답

Prompt는 단일 `Laravel\Mcp\Response` 또는 `Laravel\Mcp\Response` 인스턴스의 이터러블을 반환할 수 있습니다. 이러한 응답은 AI 클라이언트에 전송될 콘텐츠를 캡슐화합니다.

```php
<?php

namespace App\Mcp\Prompts;

use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Prompt;

class DescribeWeatherPrompt extends Prompt
{
    /**
     * Handle the prompt request.
     *
     * @return array<int, \Laravel\Mcp\Response>
     */
    public function handle(Request $request): array
    {
        $tone = $request->string('tone');

        $systemMessage = "You are a helpful weather assistant. Please provide a weather description in a {$tone} tone.";

        $userMessage = "What is the current weather like in New York City?";

        return [
            Response::text($systemMessage)->asAssistant(),
            Response::text($userMessage),
        ];
    }
}
```

`asAssistant()` 메서드를 사용하여 응답 메시지가 AI 어시스턴트로부터 온 것으로 처리되어야 함을 나타낼 수 있으며, 일반 메시지는 사용자 입력으로 처리됩니다.

<a name="resources"></a>
## 리소스 (Resources)

[Resources](https://modelcontextprotocol.io/specification/2025-06-18/server/resources)는 서버가 AI 클라이언트가 언어 모델과 상호작용할 때 컨텍스트로 읽고 사용할 수 있는 데이터와 콘텐츠를 노출할 수 있게 해줍니다. 문서, 설정 또는 AI 응답에 도움이 되는 모든 데이터와 같은 정적 또는 동적 정보를 공유하는 방법을 제공합니다.

<a name="creating-resources"></a>
## Resource 생성 (Creating Resources)

Resource를 생성하려면 `make:mcp-resource` Artisan 명령어를 실행합니다.

```shell
php artisan make:mcp-resource WeatherGuidelinesResource
```

Resource를 생성한 후에는 서버의 `$resources` 프로퍼티에 등록합니다.

```php
<?php

namespace App\Mcp\Servers;

use App\Mcp\Resources\WeatherGuidelinesResource;
use Laravel\Mcp\Server;

class WeatherServer extends Server
{
    /**
     * The resources registered with this MCP server.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Resource>>
     */
    protected array $resources = [
        WeatherGuidelinesResource::class,
    ];
}
```

<a name="resource-name-title-and-description"></a>
#### Resource 이름, 제목, 설명

기본적으로 Resource의 이름과 제목은 클래스 이름에서 자동으로 생성됩니다. 예를 들어, `WeatherGuidelinesResource`는 이름이 `weather-guidelines`이고 제목이 `Weather Guidelines Resource`가 됩니다. `Name` 및 `Title` 속성을 사용하여 이 값을 사용자 지정할 수 있습니다.

```php
use Laravel\Mcp\Server\Attributes\Name;
use Laravel\Mcp\Server\Attributes\Title;

#[Name('weather-api-docs')]
#[Title('Weather API Documentation')]
class WeatherGuidelinesResource extends Resource
{
    // ...
}
```

Resource 설명은 자동으로 생성되지 않습니다. `Description` 속성을 사용하여 항상 의미 있는 설명을 제공해야 합니다.

```php
use Laravel\Mcp\Server\Attributes\Description;

#[Description('Comprehensive guidelines for using the Weather API.')]
class WeatherGuidelinesResource extends Resource
{
    //
}
```

> [!NOTE]
> 설명은 Resource 메타데이터에서 매우 중요한 부분으로, AI 모델이 Resource를 언제 그리고 어떻게 효과적으로 사용해야 하는지 이해하는 데 도움을 줍니다.

<a name="resource-templates"></a>
### Resource 템플릿

[Resource 템플릿](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#resource-templates)은 서버가 변수가 포함된 URI 패턴과 일치하는 동적 리소스를 노출할 수 있게 해줍니다. 각 리소스에 대해 정적 URI를 정의하는 대신, 템플릿 패턴을 기반으로 여러 URI를 처리하는 단일 리소스를 만들 수 있습니다.

<a name="creating-resource-templates"></a>
#### Resource 템플릿 생성

Resource 템플릿을 생성하려면, Resource 클래스에 `HasUriTemplate` 인터페이스를 구현하고 `UriTemplate` 인스턴스를 반환하는 `uriTemplate` 메서드를 정의합니다.

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Attributes\Description;
use Laravel\Mcp\Server\Attributes\MimeType;
use Laravel\Mcp\Server\Contracts\HasUriTemplate;
use Laravel\Mcp\Server\Resource;
use Laravel\Mcp\Support\UriTemplate;

#[Description('Access user files by ID')]
#[MimeType('text/plain')]
class UserFileResource extends Resource implements HasUriTemplate
{
    /**
     * Get the URI template for this resource.
     */
    public function uriTemplate(): UriTemplate
    {
        return new UriTemplate('file://users/{userId}/files/{fileId}');
    }

    /**
     * Handle the resource request.
     */
    public function handle(Request $request): Response
    {
        $userId = $request->get('userId');
        $fileId = $request->get('fileId');

        // Fetch and return the file content...

        return Response::text($content);
    }
}
```

Resource가 `HasUriTemplate` 인터페이스를 구현하면, 정적 리소스가 아닌 리소스 템플릿으로 등록됩니다. 그러면 AI 클라이언트가 템플릿 패턴과 일치하는 URI를 사용하여 리소스를 요청할 수 있으며, URI에서 변수가 자동으로 추출되어 Resource의 `handle` 메서드에서 사용할 수 있게 됩니다.

<a name="uri-template-syntax"></a>
#### URI 템플릿 구문

URI 템플릿은 중괄호로 둘러싸인 플레이스홀더를 사용하여 URI의 변수 세그먼트를 정의합니다.

```php
new UriTemplate('file://users/{userId}');
new UriTemplate('file://users/{userId}/files/{fileId}');
new UriTemplate('https://api.example.com/{version}/{resource}/{id}');
```

<a name="accessing-template-variables"></a>
#### 템플릿 변수 접근

URI가 리소스 템플릿과 일치하면, 추출된 변수는 자동으로 요청에 병합되어 `get` 메서드를 사용하여 접근할 수 있습니다.

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Contracts\HasUriTemplate;
use Laravel\Mcp\Server\Resource;
use Laravel\Mcp\Support\UriTemplate;

class UserProfileResource extends Resource implements HasUriTemplate
{
    public function uriTemplate(): UriTemplate
    {
        return new UriTemplate('file://users/{userId}/profile');
    }

    public function handle(Request $request): Response
    {
        // Access the extracted variable
        $userId = $request->get('userId');

        // Access the full URI if needed
        $uri = $request->uri();

        // Fetch user profile...

        return Response::text("Profile for user {$userId}");
    }
}
```

`Request` 객체는 추출된 변수와 요청된 원본 URI를 모두 제공하여 리소스 요청을 처리하는 데 필요한 전체 컨텍스트를 제공합니다.

<a name="resource-uri-and-mime-type"></a>
### Resource URI 및 MIME 타입

각 Resource는 고유한 URI로 식별되며, AI 클라이언트가 리소스의 형식을 이해하는 데 도움이 되는 MIME 타입이 연결되어 있습니다.

기본적으로 Resource의 URI는 리소스 이름을 기반으로 생성되므로, `WeatherGuidelinesResource`의 URI는 `weather://resources/weather-guidelines`이 됩니다. 기본 MIME 타입은 `text/plain`입니다.

`Uri` 및 `MimeType` 속성을 사용하여 이 값을 사용자 지정할 수 있습니다.

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Server\Attributes\MimeType;
use Laravel\Mcp\Server\Attributes\Uri;
use Laravel\Mcp\Server\Resource;

#[Uri('weather://resources/guidelines')]
#[MimeType('application/pdf')]
class WeatherGuidelinesResource extends Resource
{
}
```

URI와 MIME 타입은 AI 클라이언트가 리소스 콘텐츠를 적절하게 처리하고 해석하는 방법을 결정하는 데 도움을 줍니다.

<a name="resource-request"></a>
### Resource 요청

Tool과 Prompt와 달리, Resource는 입력 스키마나 인수를 정의할 수 없습니다. 하지만 Resource의 `handle` 메서드 내에서 요청 객체와 상호작용할 수 있습니다.

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Resource;

class WeatherGuidelinesResource extends Resource
{
    /**
     * Handle the resource request.
     */
    public function handle(Request $request): Response
    {
        // ...
    }
}
```

<a name="resource-dependency-injection"></a>
### Resource 의존성 주입

모든 Resource는 Laravel [서비스 컨테이너](/docs/13.x/container)를 통해 리졸브됩니다. 따라서 Resource의 생성자에서 필요한 의존성을 타입 힌트로 지정할 수 있습니다. 선언된 의존성은 자동으로 리졸브되어 Resource 인스턴스에 주입됩니다.

```php
<?php

namespace App\Mcp\Resources;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Server\Resource;

class WeatherGuidelinesResource extends Resource
{
    /**
     * Create a new resource instance.
     */
    public function __construct(
        protected WeatherRepository $weather,
    ) {}

    // ...
}
```

생성자 주입 외에도 Resource의 `handle` 메서드에서 의존성을 타입 힌트로 지정할 수 있습니다. 서비스 컨테이너는 메서드가 호출될 때 자동으로 의존성을 리졸브하고 주입합니다.

```php
<?php

namespace App\Mcp\Resources;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Resource;

class WeatherGuidelinesResource extends Resource
{
    /**
     * Handle the resource request.
     */
    public function handle(WeatherRepository $weather): Response
    {
        $guidelines = $weather->guidelines();

        return Response::text($guidelines);
    }
}
```

<a name="resource-annotations"></a>
### Resource 어노테이션

[어노테이션](https://modelcontextprotocol.io/specification/2025-06-18/schema#resourceannotations)을 사용하여 AI 클라이언트에 추가 메타데이터를 제공함으로써 Resource를 향상시킬 수 있습니다. 어노테이션은 속성(attribute)을 통해 Resource에 추가됩니다.

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Enums\Role;
use Laravel\Mcp\Server\Annotations\Audience;
use Laravel\Mcp\Server\Annotations\LastModified;
use Laravel\Mcp\Server\Annotations\Priority;
use Laravel\Mcp\Server\Resource;

#[Audience(Role::User)]
#[LastModified('2025-01-12T15:00:58Z')]
#[Priority(0.9)]
class UserDashboardResource extends Resource
{
    //
}
```

사용 가능한 어노테이션은 다음과 같습니다.

| 어노테이션 | 타입 | 설명 |
| --- | --- | --- |
| `#[Audience]` | Role 또는 array | 대상 사용자를 지정합니다(`Role::User`, `Role::Assistant`, 또는 둘 다). |
| `#[Priority]` | float | 리소스 중요도를 나타내는 0.0에서 1.0 사이의 숫자 점수입니다. |
| `#[LastModified]` | string | 리소스가 마지막으로 업데이트된 시점을 나타내는 ISO 8601 타임스탬프입니다. |

<a name="conditional-resource-registration"></a>
### 조건부 Resource 등록

Resource 클래스에 `shouldRegister` 메서드를 구현하여 런타임에 조건부로 Resource를 등록할 수 있습니다. 이 메서드를 사용하면 애플리케이션 상태, 설정 또는 요청 파라미터에 따라 Resource의 사용 가능 여부를 결정할 수 있습니다.

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Request;
use Laravel\Mcp\Server\Resource;

class WeatherGuidelinesResource extends Resource
{
    /**
     * Determine if the resource should be registered.
     */
    public function shouldRegister(Request $request): bool
    {
        return $request?->user()?->subscribed() ?? false;
    }
}
```

Resource의 `shouldRegister` 메서드가 `false`를 반환하면, 사용 가능한 Resource 목록에 표시되지 않으며 AI 클라이언트가 접근할 수 없습니다.

<a name="resource-responses"></a>
### Resource 응답

Resource는 반드시 `Laravel\Mcp\Response` 인스턴스를 반환해야 합니다. Response 클래스는 다양한 유형의 응답을 생성하기 위한 여러 편리한 메서드를 제공합니다.

단순 텍스트 콘텐츠의 경우 `text` 메서드를 사용합니다.

```php
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;

/**
 * Handle the resource request.
 */
public function handle(Request $request): Response
{
    // ...

    return Response::text($weatherData);
}
```

<a name="resource-blob-responses"></a>
#### Blob 응답

Blob 콘텐츠를 반환하려면 `blob` 메서드를 사용하여 Blob 콘텐츠를 제공합니다.

```php
return Response::blob(file_get_contents(storage_path('weather/radar.png')));
```

Blob 콘텐츠를 반환할 때, MIME 타입은 Resource에 설정된 MIME 타입에 의해 결정됩니다.

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Server\Attributes\MimeType;
use Laravel\Mcp\Server\Resource;

#[MimeType('image/png')]
class WeatherGuidelinesResource extends Resource
{
    //
}
```

<a name="resource-error-responses"></a>
#### 오류 응답

리소스 검색 중 오류가 발생했음을 나타내려면 `error()` 메서드를 사용합니다.

```php
return Response::error('Unable to fetch weather data for the specified location.');
```

<a name="metadata"></a>
## 메타데이터 (Metadata)

Laravel MCP는 [MCP 사양](https://modelcontextprotocol.io/specification/2025-06-18/basic#meta)에 정의된 `_meta` 필드도 지원하며, 이는 특정 MCP 클라이언트나 통합에서 필요합니다. 메타데이터는 Tool, Resource, Prompt를 포함한 모든 MCP 프리미티브와 그 응답에 적용할 수 있습니다.

`withMeta` 메서드를 사용하여 개별 응답 콘텐츠에 메타데이터를 첨부할 수 있습니다.

```php
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;

/**
 * Handle the tool request.
 */
public function handle(Request $request): Response
{
    return Response::text('The weather is sunny.')
        ->withMeta(['source' => 'weather-api', 'cached' => true]);
}
```

전체 응답 엔벨로프에 적용되는 결과 수준 메타데이터의 경우, `Response::make`로 응답을 감싸고 반환된 Response 팩토리 인스턴스에서 `withMeta`를 호출합니다.

```php
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\ResponseFactory;

/**
 * Handle the tool request.
 */
public function handle(Request $request): ResponseFactory
{
    return Response::make(
        Response::text('The weather is sunny.')
    )->withMeta(['request_id' => '12345']);
}
```

Tool, Resource 또는 Prompt 자체에 메타데이터를 첨부하려면 클래스에 `$meta` 프로퍼티를 정의합니다.

```php
use Laravel\Mcp\Server\Attributes\Description;
use Laravel\Mcp\Server\Tool;

#[Description('Fetches the current weather forecast.')]
class CurrentWeatherTool extends Tool
{
    protected ?array $meta = [
        'version' => '2.0',
        'author' => 'Weather Team',
    ];

    // ...
}
```

<a name="authentication"></a>
## 인증 (Authentication)

라우트와 마찬가지로, 미들웨어를 사용하여 웹 MCP 서버를 인증할 수 있습니다. MCP 서버에 인증을 추가하면 사용자가 서버의 모든 기능을 사용하기 전에 인증을 수행해야 합니다.

MCP 서버에 대한 접근을 인증하는 방법은 두 가지가 있습니다. [Laravel Sanctum](/docs/13.x/sanctum)을 사용한 간단한 토큰 기반 인증 또는 `Authorization` HTTP 헤더를 통해 전달되는 토큰을 사용하는 방법, 그리고 [Laravel Passport](/docs/13.x/passport)를 사용한 OAuth 인증입니다.

<a name="oauth"></a>
### OAuth 2.1

웹 기반 MCP 서버를 보호하는 가장 강력한 방법은 [Laravel Passport](/docs/13.x/passport)를 사용한 OAuth입니다.

OAuth를 통해 MCP 서버를 인증할 때, `routes/ai.php` 파일에서 `Mcp::oauthRoutes` 메서드를 호출하여 필요한 OAuth2 디스커버리 및 클라이언트 등록 라우트를 등록합니다. 그런 다음 `routes/ai.php` 파일의 `Mcp::web` 라우트에 Passport의 `auth:api` 미들웨어를 적용합니다.

```php
use App\Mcp\Servers\WeatherExample;
use Laravel\Mcp\Facades\Mcp;

Mcp::oauthRoutes();

Mcp::web('/mcp/weather', WeatherExample::class)
    ->middleware('auth:api');
```

#### 새로운 Passport 설치

애플리케이션에서 아직 Laravel Passport를 사용하지 않는 경우, Passport의 [설치 및 배포 가이드](/docs/13.x/passport#installation)를 따라 애플리케이션에 Passport를 추가하세요. 진행하기 전에 `OAuthenticatable` 모델, 새로운 인증 가드, Passport 키가 준비되어 있어야 합니다.

다음으로, Laravel MCP가 제공하는 Passport 인가 뷰를 퍼블리싱해야 합니다.

```shell
php artisan vendor:publish --tag=mcp-views
```

그런 다음 `Passport::authorizationView` 메서드를 사용하여 Passport가 이 뷰를 사용하도록 지시합니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출해야 합니다.

```php
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::authorizationView(function ($parameters) {
        return view('mcp.authorize', $parameters);
    });
}
```

이 뷰는 인증 과정에서 최종 사용자에게 표시되어 AI 에이전트의 인증 시도를 승인하거나 거부할 수 있게 합니다.

![Authorization screen example](data:image/png;base64,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)

> [!NOTE]
> 이 시나리오에서는 단순히 OAuth를 기본 인증 가능 모델에 대한 변환 계층으로 사용하고 있습니다. 스코프와 같은 OAuth의 많은 측면은 무시됩니다.

#### 기존 Passport 설치 사용

애플리케이션에서 이미 Laravel Passport를 사용하고 있는 경우, Laravel MCP는 기존 Passport 설치와 원활하게 작동합니다. 다만 OAuth가 주로 기본 인증 가능 모델에 대한 변환 계층으로 사용되므로 커스텀 스코프는 현재 지원되지 않습니다.

Laravel MCP는 위에서 설명한 `Mcp::oauthRoutes` 메서드를 통해 단일 `mcp:use` 스코프를 추가하고, 알리며, 사용합니다.

#### Passport vs. Sanctum

OAuth2.1은 Model Context Protocol 사양에 문서화된 인증 메커니즘이며, MCP 클라이언트 간에 가장 널리 지원됩니다. 따라서 가능한 경우 Passport 사용을 권장합니다.

애플리케이션에서 이미 [Sanctum](/docs/13.x/sanctum)을 사용하고 있다면 Passport를 추가하는 것이 번거로울 수 있습니다. 이 경우에는 OAuth만 지원하는 MCP 클라이언트를 사용해야 하는 명확하고 필수적인 요구사항이 생기기 전까지는 Passport 없이 Sanctum을 사용하는 것을 권장합니다.

<a name="sanctum"></a>
### Sanctum

[Sanctum](/docs/13.x/sanctum)을 사용하여 MCP 서버를 보호하려면, `routes/ai.php` 파일에서 서버에 Sanctum의 인증 미들웨어를 추가하기만 하면 됩니다. 그런 다음 MCP 클라이언트가 인증 성공을 위해 `Authorization: Bearer <token>` 헤더를 제공하도록 합니다.

```php
use App\Mcp\Servers\WeatherExample;
use Laravel\Mcp\Facades\Mcp;

Mcp::web('/mcp/demo', WeatherExample::class)
    ->middleware('auth:sanctum');
```

<a name="custom-mcp-authentication"></a>
#### 커스텀 MCP 인증

애플리케이션이 자체 커스텀 API 토큰을 발급하는 경우, `Mcp::web` 라우트에 원하는 미들웨어를 할당하여 MCP 서버를 인증할 수 있습니다. 커스텀 미들웨어는 `Authorization` 헤더를 수동으로 검사하여 들어오는 MCP 요청을 인증할 수 있습니다.

<a name="authorization"></a>
## 인가 (Authorization)

`$request->user()` 메서드를 통해 현재 인증된 사용자에 접근하여 MCP Tool과 Resource 내에서 [인가 확인](/docs/13.x/authorization)을 수행할 수 있습니다.

```php
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;

/**
 * Handle the tool request.
 */
public function handle(Request $request): Response
{
    if (! $request->user()->can('read-weather')) {
        return Response::error('Permission denied.');
    }

    // ...
}
```

<a name="testing-servers"></a>
## 서버 테스트 (Testing Servers)

내장된 MCP Inspector를 사용하거나 유닛 테스트를 작성하여 MCP 서버를 테스트할 수 있습니다.

<a name="mcp-inspector"></a>
### MCP Inspector

[MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector)는 MCP 서버를 테스트하고 디버깅하기 위한 대화형 도구입니다. 서버에 연결하고, 인증을 확인하고, Tool, Resource, Prompt를 시험해 볼 수 있습니다.

등록된 모든 서버에 대해 Inspector를 실행할 수 있습니다.

```shell
# Web server...
php artisan mcp:inspector mcp/weather

# Local server named "weather"...
php artisan mcp:inspector weather
```

이 명령어는 MCP Inspector를 실행하고, MCP 클라이언트에 복사할 수 있는 클라이언트 설정을 제공하여 모든 것이 올바르게 구성되었는지 확인할 수 있습니다. 웹 서버가 인증 미들웨어로 보호되어 있는 경우, 연결 시 `Authorization` 베어러 토큰과 같은 필수 헤더를 포함해야 합니다.

<a name="unit-tests"></a>
### 유닛 테스트

MCP 서버, Tool, Resource, Prompt에 대한 유닛 테스트를 작성할 수 있습니다.

시작하려면, 새로운 테스트 케이스를 생성하고 해당 프리미티브를 등록한 서버에서 원하는 프리미티브를 호출합니다. 예를 들어, `WeatherServer`의 Tool을 테스트하려면 다음과 같이 합니다.

```php tab=Pest
test('tool', function () {
    $response = WeatherServer::tool(CurrentWeatherTool::class, [
        'location' => 'New York City',
        'units' => 'fahrenheit',
    ]);

    $response
        ->assertOk()
        ->assertSee('The current weather in New York City is 72°F and sunny.');
});
```

```php tab=PHPUnit
/**
 * Test a tool.
 */
public function test_tool(): void
{
    $response = WeatherServer::tool(CurrentWeatherTool::class, [
        'location' => 'New York City',
        'units' => 'fahrenheit',
    ]);

    $response
        ->assertOk()
        ->assertSee('The current weather in New York City is 72°F and sunny.');
}
```

마찬가지로 Prompt와 Resource를 테스트할 수 있습니다.

```php
$response = WeatherServer::prompt(...);
$response = WeatherServer::resource(...);
```

프리미티브를 호출하기 전에 `actingAs` 메서드를 체이닝하여 인증된 사용자로 동작할 수도 있습니다.

```php
$response = WeatherServer::actingAs($user)->tool(...);
```

응답을 받은 후, 다양한 어설션 메서드를 사용하여 응답의 콘텐츠와 상태를 확인할 수 있습니다.

`assertOk` 메서드를 사용하여 응답이 성공적인지 확인할 수 있습니다. 이 메서드는 응답에 오류가 없는지 검사합니다.

```php
$response->assertOk();
```

`assertSee` 메서드를 사용하여 응답에 특정 텍스트가 포함되어 있는지 확인할 수 있습니다.

```php
$response->assertSee('The current weather in New York City is 72°F and sunny.');
```

`assertHasErrors` 메서드를 사용하여 응답에 오류가 포함되어 있는지 확인할 수 있습니다.

```php
$response->assertHasErrors();

$response->assertHasErrors([
    'Something went wrong.',
]);
```

`assertHasNoErrors` 메서드를 사용하여 응답에 오류가 포함되어 있지 않은지 확인할 수 있습니다.

```php
$response->assertHasNoErrors();
```

`assertName()`, `assertTitle()`, `assertDescription()` 메서드를 사용하여 응답에 특정 메타데이터가 포함되어 있는지 확인할 수 있습니다.

```php
$response->assertName('current-weather');
$response->assertTitle('Current Weather Tool');
$response->assertDescription('Fetches the current weather forecast for a specified location.');
```

`assertSentNotification` 및 `assertNotificationCount` 메서드를 사용하여 알림이 전송되었는지 확인할 수 있습니다.

```php
$response->assertSentNotification('processing/progress', [
    'step' => 1,
    'total' => 5,
]);

$response->assertSentNotification('processing/progress', [
    'step' => 2,
    'total' => 5,
]);

$response->assertNotificationCount(5);
```

마지막으로, 원시 응답 콘텐츠를 검사하려면 `dd` 또는 `dump` 메서드를 사용하여 디버깅 목적으로 응답을 출력할 수 있습니다.

```php
$response->dd();
$response->dump();
```
