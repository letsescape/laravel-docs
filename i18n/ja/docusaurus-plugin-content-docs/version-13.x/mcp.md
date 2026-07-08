<!-- # Laravel MCP -->
# Laravel MCP

- [Introduction](#introduction)
- [Installation](#installation)
    - [Publishing Routes](#publishing-routes)
- [Creating Servers](#creating-servers)
    - [Server Registration](#server-registration)
    - [Web Servers](#web-servers)
    - [Local Servers](#local-servers)
- [Tools](#tools)
    - [Creating Tools](#creating-tools)
    - [Tool Input Schemas](#tool-input-schemas)
    - [Tool Output Schemas](#tool-output-schemas)
    - [Validating Tool Arguments](#validating-tool-arguments)
    - [Tool Dependency Injection](#tool-dependency-injection)
    - [Tool Annotations](#tool-annotations)
    - [Conditional Tool Registration](#conditional-tool-registration)
    - [Tool Responses](#tool-responses)
- [Prompts](#prompts)
    - [Creating Prompts](#creating-prompts)
    - [Prompt Arguments](#prompt-arguments)
    - [Validating Prompt Arguments](#validating-prompt-arguments)
    - [Prompt Dependency Injection](#prompt-dependency-injection)
    - [Conditional Prompt Registration](#conditional-prompt-registration)
    - [Prompt Responses](#prompt-responses)
- [Resources](#resources)
    - [Creating Resources](#creating-resources)
    - [Resource Templates](#resource-templates)
    - [Resource URI and MIME Type](#resource-uri-and-mime-type)
    - [Resource Request](#resource-request)
    - [Resource Dependency Injection](#resource-dependency-injection)
    - [Resource Annotations](#resource-annotations)
    - [Conditional Resource Registration](#conditional-resource-registration)
    - [Resource Responses](#resource-responses)
- [Apps](#apps)
    - [Creating App Resources](#creating-app-resources)
    - [Rendering Apps From Tools](#rendering-apps-from-tools)
    - [App Tool Visibility](#app-tool-visibility)
    - [App Configuration](#app-configuration)
    - [Building Apps With Boost](#building-apps-with-boost)
- [Metadata](#metadata)
- [Icons](#icons)
- [Authentication](#authentication)
    - [OAuth 2.1](#oauth)
    - [Sanctum](#sanctum)
- [Authorization](#authorization)
- [MCP Client](#client)
    - [Connecting to Servers](#client-connecting)
    - [Named Clients](#named-clients)
    - [Client Authentication](#client-authentication)
    - [Tools](#client-tools)
    - [Prompts](#client-prompts)
    - [Resources](#client-resources)
- [Testing Servers](#testing-servers)
    - [MCP Inspector](#mcp-inspector)
    - [Unit Tests](#unit-tests)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel MCP](https://github.com/laravel/mcp) provides a simple and elegant way for AI clients to interact with your Laravel application through the [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro). It offers an expressive, fluent interface for defining servers, tools, resources, and prompts that enable AI-powered interactions with your application. -->
[Laravel MCP](https://github.com/laravel/mcp) は、AI クライアントが [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro) を通じて Laravel アプリケーションと対話するためのシンプルかつエレガントな方法を提供します。サーバー、ツール、リソース、プロンプトを定義するための表現力豊かで流暢なインターフェイスを提供し、AI を活用したアプリケーションとの対話を可能にします。

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- To get started, install Laravel MCP into your project using the Composer package manager: -->
まず、Composer パッケージ マネージャーを使用して Laravel MCP をプロジェクトにインストールします。

```shell
composer require laravel/mcp
```

<a name="publishing-routes"></a>
<!-- ### Publishing Routes -->
### Publishing Routes

<!-- After installing Laravel MCP, execute the `vendor:publish` Artisan command to publish the `routes/ai.php` file where you will define your MCP servers: -->
Laravel MCP をインストールした後、`vendor:publish` Artisan コマンドを実行して、MCP サーバーを定義する `routes/ai.php` ファイルを公開します。

```shell
php artisan vendor:publish --tag=ai-routes
```

<!-- This command creates the `routes/ai.php` file in your application's `routes` directory, which you will use to register your MCP servers. -->
このコマンドは、アプリケーションの `routes` ディレクトリに `routes/ai.php` ファイルを作成します。このファイルは、MCP サーバーの登録に使用されます。

<a name="creating-servers"></a>
<!-- ## Creating Servers -->
## Creating Servers

<!-- You can create an MCP server using the `make:mcp-server` Artisan command. Servers act as the central communication point that exposes MCP capabilities like tools, resources, and prompts to AI clients: -->
`make:mcp-server` Artisan コマンドを使用して MCP サーバーを作成できます。サーバーは、ツール、リソース、プロンプトなどの MCP 機能を AI クライアントに公開する中央の通信ポイントとして機能します。

```shell
php artisan make:mcp-server WeatherServer
```

<!-- This command will create a new server class in the `app/Mcp/Servers` directory. The generated server class extends Laravel MCP's base `Laravel\Mcp\Server` class and provides attributes and properties for configuring the server and registering tools, resources, and prompts: -->
このコマンドは、`app/Mcp/Servers` ディレクトリに新しいサーバー クラスを作成します。生成されたサーバークラスは、Laravel MCP の基本 `Laravel\Mcp\Server` クラスを拡張し、サーバーを構成し、ツール、リソース、プロンプトを登録するための属性とプロパティを提供します。

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
<!-- ### Server Registration -->
### Server Registration

<!-- Once you've created a server, you must register it in your `routes/ai.php` file to make it accessible. Laravel MCP provides two methods for registering servers: `web` for HTTP-accessible servers and `local` for command-line servers. -->
サーバーを作成したら、それを `routes/ai.php` ファイルに登録してアクセスできるようにする必要があります。 Laravel MCP は、サーバーを登録するための 2 つの方法を提供します。HTTP アクセス可能なサーバー用の `web` と、コマンドライン サーバー用の `local` です。

<a name="web-servers"></a>
<!-- ### Web Servers -->
### Web Servers

<!-- Web servers are the most common types of servers and are accessible via HTTP POST requests, making them ideal for remote AI clients or web-based integrations. Register a web server using the `web` method: -->
Web サーバーは最も一般的なタイプのサーバーであり、HTTP POST リクエスト経由でアクセスできるため、リモート AI クライアントまたは Web ベースの統合に最適です。 `web` メソッドを使用して Web サーバーを登録します。

```php
use App\Mcp\Servers\WeatherServer;
use Laravel\Mcp\Facades\Mcp;

Mcp::web('/mcp/weather', WeatherServer::class);
```

<!-- Just like normal routes, you may apply middleware to protect your web servers: -->
通常のルートと同様に、ミドルウェアを適用して Web サーバーを保護できます。

```php
Mcp::web('/mcp/weather', WeatherServer::class)
    ->middleware(['throttle:mcp']);
```

<a name="local-servers"></a>
<!-- ### Local Servers -->
### Local Servers

<!-- Local servers run as Artisan commands, perfect for building local AI assistant integrations like [Laravel Boost](/docs/13.x/installation#installing-laravel-boost). Register a local server using the `local` method: -->
ローカル サーバーは Artisan コマンドとして実行され、[Laravel Boost](/docs/13.x/installation#installing-laravel-boost) のようなローカル AI アシスタント統合の構築に最適です。 `local` メソッドを使用してローカル サーバーを登録します。

```php
use App\Mcp\Servers\WeatherServer;
use Laravel\Mcp\Facades\Mcp;

Mcp::local('weather', WeatherServer::class);
```

<!-- Once registered, you should not typically need to manually run the `mcp:start` Artisan command yourself. Instead, configure your MCP client (AI agent) to start the server or use the [MCP Inspector](#mcp-inspector). -->
一度登録すると、通常は `mcp:start` Artisan コマンドを自分で手動で実行する必要はありません。代わりに、サーバーを起動するか、[MCP Inspector](#mcp-inspector) を使用するように MCP クライアント (AI エージェント) を構成します。

<a name="tools"></a>
<!-- ## Tools -->
## Tools

<!-- Tools enable your server to expose functionality that AI clients can call. They allow language models to perform actions, run code, or interact with external systems: -->
ツールを使用すると、サーバーは AI クライアントが呼び出すことができる機能を公開できます。これらにより、言語モデルがアクションを実行したり、コードを実行したり、外部システムと対話したりできるようになります。

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
<!-- ### Creating Tools -->
### Creating Tools

<!-- To create a tool, run the `make:mcp-tool` Artisan command: -->
ツールを作成するには、`make:mcp-tool` Artisan コマンドを実行します。

```shell
php artisan make:mcp-tool CurrentWeatherTool
```

<!-- After creating a tool, register it in your server's `$tools` property: -->
ツールを作成したら、それをサーバーの `$tools` プロパティに登録します。

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
<!-- #### Tool Name, Title, and Description -->
#### Tool Name, Title, and Description

<!-- By default, the tool's name and title are derived from the class name. For example, `CurrentWeatherTool` will have a name of `current-weather` and a title of `Current Weather Tool`. You may customize these values using the `Name` and `Title` attributes: -->
デフォルトでは、ツールの名前とタイトルはクラス名から派生します。たとえば、`CurrentWeatherTool` の名前は `current-weather`、タイトルは `Current Weather Tool` になります。これらの値は、`Name` 属性と `Title` 属性を使用してカスタマイズできます。

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

<!-- Tool descriptions are not automatically generated. You should always provide a meaningful description using the `Description` attribute: -->
ツールの説明は自動生成されません。常に `Description` 属性を使用して意味のある説明を提供する必要があります。

```php
use Laravel\Mcp\Server\Attributes\Description;

#[Description('Fetches the current weather forecast for a specified location.')]
class CurrentWeatherTool extends Tool
{
    //
}
```

> [!NOTE]
> 説明はツールのメタデータの重要な部分であり、AI モデルがツールをいつどのように効果的に使用するかを理解するのに役立ちます。

<a name="tool-input-schemas"></a>
<!-- ### Tool Input Schemas -->
### Tool Input Schemas

<!-- Tools can define input schemas to specify what arguments they accept from AI clients. Use Laravel's `Illuminate\Contracts\JsonSchema\JsonSchema` builder to define your tool's input requirements: -->
ツールは入力スキーマを定義して、AI クライアントから受け入れる引数を指定できます。 Laravel の `Illuminate\Contracts\JsonSchema\JsonSchema` ビルダを使用して、ツールの入力要件を定義します。

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
<!-- ### Tool Output Schemas -->
### Tool Output Schemas

<!-- Tools can define [output schemas](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#output-schema) to specify the structure of their responses. This enables better integration with AI clients that need parseable tool results. Use the `outputSchema` method to define your tool's output structure: -->
ツールは [output schemas](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#output-schema) を定義して応答の構造を指定できます。これにより、解析可能なツール結果を必要とする AI クライアントとの統合が可能になります。 `outputSchema` メソッドを使用して、ツールの出力構造を定義します。

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
<!-- ### Validating Tool Arguments -->
### Validating Tool Arguments

<!-- JSON Schema definitions provide a basic structure for tool arguments, but you may also want to enforce more complex validation rules. -->
JSON スキーマ定義はツール引数の基本構造を提供しますが、より複雑な検証ルールを強制することもできます。

<!-- Laravel MCP integrates seamlessly with Laravel's [validation features](/docs/13.x/validation). You may validate incoming tool arguments within your tool's `handle` method: -->
Laravel MCP は、Laravel の [validation features](/docs/13.x/validation) とシームレスに統合されます。ツールの `handle` メソッド内で受信ツール引数を検証できます。

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

<!-- On validation failure, AI clients will act based on the error messages you provide. As such, it is critical to provide clear and actionable error messages: -->
検証が失敗すると、AI クライアントは提供されたエラー メッセージに基づいて動作します。したがって、明確で実用的なエラー メッセージを提供することが重要です。

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
<!-- #### Tool Dependency Injection -->
#### Tool Dependency Injection

<!-- The Laravel [service container](/docs/13.x/container) is used to resolve all tools. As a result, you are able to type-hint any dependencies your tool may need in its constructor. The declared dependencies will automatically be resolved and injected into the tool instance: -->
Laravel [service container](/docs/13.x/container) は、すべてのツールを解決するために使用されます。その結果、ツールのコンストラクターで必要な依存関係をタイプヒントで指定できるようになります。宣言された依存関係は自動的に解決され、ツール インスタンスに挿入されます。

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

<!-- In addition to constructor injection, you may also type-hint dependencies in your tool's `handle()` method. The service container will automatically resolve and inject the dependencies when the method is called: -->
コンストラクターの注入に加えて、ツールの `handle()` メソッドでタイプヒントの依存関係を指定することもできます。サービスコンテナーは、メソッドが呼び出されるときに依存関係を自動的に解決して挿入します。

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
<!-- ### Tool Annotations -->
### Tool Annotations

<!-- You may enhance your tools with [annotations](https://modelcontextprotocol.io/specification/2025-06-18/schema#toolannotations) to provide additional metadata to AI clients. These annotations help AI models understand the tool's behavior and capabilities. Annotations are added to tools via attributes: -->
[annotations](https://modelcontextprotocol.io/specification/2025-06-18/schema#toolannotations) を使用してツールを強化し、AI クライアントに追加のメタデータを提供できます。これらの注釈は、AI モデルがツールの動作と機能を理解するのに役立ちます。注釈は属性を介してツールに追加されます。

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

<!-- Available annotations include: -->
利用可能な注釈は次のとおりです。

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| 注釈         | タイプ    | 説明                                                                                  |
| ------------------ | ------- | -------------------------------------------------------------------------------------------- |
| `#[IsReadOnly]`    | ブール値 | ツールが環境を変更しないことを示します。                                          |
| `#[IsDestructive]` | ブール値 | ツールが破壊的な更新を実行する可能性があることを示します (読み取り専用でない場合にのみ意味があります)。     |
| `#[IsIdempotent]`  | ブール値 | 同じ引数で繰り返し呼び出しても追加の効果がないことを示します (読み取り専用でない場合)。 |
| `#[IsOpenWorld]`   | ブール値 | ツールが外部エンティティと対話する可能性があることを示します。                                      |

<!-- </div> -->
</div>

<!-- Annotation values can be explicitly set using boolean arguments: -->
注釈値は、ブール引数を使用して明示的に設定できます。

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
<!-- ### Conditional Tool Registration -->
### Conditional Tool Registration

<!-- You may conditionally register tools at runtime by implementing the `shouldRegister` method in your tool class. This method allows you to determine whether a tool should be available based on application state, configuration, or request parameters: -->
ツール クラスに `shouldRegister` メソッドを実装することで、実行時に条件付きでツールを登録できます。この方法を使用すると、アプリケーションの状態、構成、またはリクエスト パラメーターに基づいてツールを使用可能にするかどうかを決定できます。

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

<!-- When a tool's `shouldRegister` method returns `false`, it will not appear in the list of available tools and cannot be invoked by AI clients. -->
ツールの `shouldRegister` メソッドが `false` を返した場合、そのツールは使用可能なツールのリストに表示されず、AI クライアントから呼び出すことはできません。

<a name="tool-responses"></a>
<!-- ### Tool Responses -->
### Tool Responses

<!-- Tools must return an instance of `Laravel\Mcp\Response`. The Response class provides several convenient methods for creating different types of responses: -->
ツールは `Laravel\Mcp\Response` のインスタンスを返す必要があります。 Response クラスには、さまざまな種類の応答を作成するための便利なメソッドがいくつか用意されています。

<!-- For simple text responses, use the `text` method: -->
単純なテキスト応答の場合は、`text` メソッドを使用します。

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

<!-- To indicate an error occurred during tool execution, use the `error` method: -->
ツールの実行中にエラーが発生したことを示すには、`error` メソッドを使用します。

```php
return Response::error('Unable to fetch weather data. Please try again.');
```

<!-- To return image or audio content, use the `image` and `audio` methods: -->
画像または音声コンテンツを返すには、`image` メソッドと `audio` メソッドを使用します。

```php
return Response::image(file_get_contents(storage_path('weather/radar.png')), 'image/png');

return Response::audio(file_get_contents(storage_path('weather/alert.mp3')), 'audio/mp3');
```

<!-- You may also load image and audio content directly from a Laravel filesystem disk using the `fromStorage` method. The MIME type will be automatically detected from the file: -->
`fromStorage` メソッドを使用して、Laravel ファイルシステム ディスクから画像と音声のコンテンツを直接ロードすることもできます。 MIME タイプはファイルから自動的に検出されます。

```php
return Response::fromStorage('weather/radar.png');
```

<!-- If needed, you may specify a particular disk or override the MIME type: -->
必要に応じて、特定のディスクを指定するか、MIME タイプをオーバーライドできます。

```php
return Response::fromStorage('weather/radar.png', disk: 's3');

return Response::fromStorage('weather/radar.png', mimeType: 'image/webp');
```

<a name="multiple-content-responses"></a>
<!-- #### Multiple Content Responses -->
#### Multiple Content Responses

<!-- Tools can return multiple pieces of content by returning an array of `Response` instances: -->
ツールは、`Response` インスタンスの配列を返すことで、複数のコンテンツを返すことができます。

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
        Response::text("**Detailed Forecast**\n- Morning: 65°F\n- Afternoon: 78°F\n- Evening: 70°F")
    ];
}
```

<a name="structured-responses"></a>
<!-- #### Structured Responses -->
#### Structured Responses

<!-- Tools can return [structured content](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#structured-content) using the `structured` method. This provides parseable data for AI clients while maintaining backward compatibility with a JSON-encoded text representation: -->
ツールは、`structured` メソッドを使用して [structured content](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#structured-content) を返すことができます。これにより、JSON エンコードされたテキスト表現との下位互換性を維持しながら、AI クライアントに解析可能なデータが提供されます。

```php
return Response::structured([
    'temperature' => 22.5,
    'conditions' => 'Partly cloudy',
    'humidity' => 65,
]);
```

<!-- If you need to provide custom text alongside structured content, use the `withStructuredContent` method on the response factory: -->
構造化コンテンツと一緒にカスタム テキストを提供する必要がある場合は、レスポンス ファクトリで `withStructuredContent` メソッドを使用します。

```php
return Response::make(
    Response::text('Weather is 22.5°C and sunny')
)->withStructuredContent([
    'temperature' => 22.5,
    'conditions' => 'Sunny',
]);
```

<a name="streaming-responses"></a>
<!-- #### Streaming Responses -->
#### Streaming Responses

<!-- For long-running operations or real-time data streaming, tools can return a [generator](https://www.php.net/manual/en/language.generators.overview.php) from their `handle` method. This enables sending intermediate updates to the client before the final response: -->
長時間実行される操作またはリアルタイム データ ストリーミングの場合、ツールは `handle` メソッドから [generator](https://www.php.net/manual/en/language.generators.overview.php) を返すことができます。これにより、最終応答の前に中間更新をクライアントに送信できるようになります。

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

<!-- When using web-based servers, streaming responses automatically open an SSE (Server-Sent Events) stream, sending each yielded message as an event to the client. -->
Web ベースのサーバーを使用する場合、ストリーミング応答は自動的に SSE (Server-Sent Events) ストリームを開き、生成された各メッセージをイベントとしてクライアントに送信します。

<a name="prompts"></a>
<!-- ## Prompts -->
## Prompts

<!-- [Prompts](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts) enable your server to share reusable prompt templates that AI clients can use to interact with language models. They provide a standardized way to structure common queries and interactions. -->
[Prompts](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts) を使用すると、AI クライアントが言語モデルと対話するために使用できる再利用可能なプロンプト テンプレートをサーバーで共有できるようになります。これらは、一般的なクエリと対話を構造化するための標準化された方法を提供します。

<a name="creating-prompts"></a>
<!-- ### Creating Prompts -->
### Creating Prompts

<!-- To create a prompt, run the `make:mcp-prompt` Artisan command: -->
プロンプトを作成するには、`make:mcp-prompt` Artisan コマンドを実行します。

```shell
php artisan make:mcp-prompt DescribeWeatherPrompt
```

<!-- After creating a prompt, register it in your server's `$prompts` property: -->
プロンプトを作成したら、それをサーバーの `$prompts` プロパティに登録します。

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
<!-- #### Prompt Name, Title, and Description -->
#### Prompt Name, Title, and Description

<!-- By default, the prompt's name and title are derived from the class name. For example, `DescribeWeatherPrompt` will have a name of `describe-weather` and a title of `Describe Weather Prompt`. You may customize these values using the `Name` and `Title` attributes: -->
デフォルトでは、プロンプトの名前とタイトルはクラス名から派生します。たとえば、`DescribeWeatherPrompt` の名前は `describe-weather`、タイトルは `Describe Weather Prompt` になります。これらの値は、`Name` 属性と `Title` 属性を使用してカスタマイズできます。

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

<!-- Prompt descriptions are not automatically generated. You should always provide a meaningful description using the `Description` attribute: -->
プロンプトの説明は自動的には生成されません。常に `Description` 属性を使用して意味のある説明を提供する必要があります。

```php
use Laravel\Mcp\Server\Attributes\Description;

#[Description('Generates a natural-language explanation of the weather for a given location.')]
class DescribeWeatherPrompt extends Prompt
{
    //
}
```

> [!NOTE]
> 説明は、AI モデルがプロンプトをいつどのように最大限に活用するかを理解するのに役立つため、プロンプトのメタデータの重要な部分です。

<a name="prompt-arguments"></a>
<!-- ### Prompt Arguments -->
### Prompt Arguments

<!-- Prompts can define arguments that allow AI clients to customize the prompt template with specific values. Use the `arguments` method to define what arguments your prompt accepts: -->
プロンプトでは、AI クライアントが特定の値を使用してプロンプト テンプレートをカスタマイズできるようにする引数を定義できます。 `arguments` メソッドを使用して、プロンプトが受け入れる引数を定義します。

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
<!-- ### Validating Prompt Arguments -->
### Validating Prompt Arguments

<!-- Prompt arguments are automatically validated based on their definition, but you may also want to enforce more complex validation rules. -->
プロンプト引数はその定義に基づいて自動的に検証されますが、より複雑な検証ルールを適用することもできます。

<!-- Laravel MCP integrates seamlessly with Laravel's [validation features](/docs/13.x/validation). You may validate incoming prompt arguments within your prompt's `handle` method: -->
Laravel MCP は、Laravel の [validation features](/docs/13.x/validation) とシームレスに統合されます。プロンプトの `handle` メソッド内で受信プロンプト引数を検証できます。

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

<!-- On validation failure, AI clients will act based on the error messages you provide. As such, it is critical to provide clear and actionable error messages: -->
検証が失敗すると、AI クライアントは提供されたエラー メッセージに基づいて動作します。したがって、明確で実用的なエラー メッセージを提供することが重要です。

```php
$validated = $request->validate([
    'tone' => ['required','string','max:50'],
],[
    'tone.*' => 'You must specify a tone for the weather description. Examples include "formal", "casual", or "humorous".',
]);
```

<a name="prompt-dependency-injection"></a>
<!-- ### Prompt Dependency Injection -->
### Prompt Dependency Injection

<!-- The Laravel [service container](/docs/13.x/container) is used to resolve all prompts. As a result, you are able to type-hint any dependencies your prompt may need in its constructor. The declared dependencies will automatically be resolved and injected into the prompt instance: -->
Laravel [service container](/docs/13.x/container) は、すべてのプロンプトを解決するために使用されます。その結果、プロンプトのコンストラクターで必要な依存関係をタイプヒントで指定できるようになります。宣言された依存関係は自動的に解決され、プロンプト インスタンスに挿入されます。

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

<!-- In addition to constructor injection, you may also type-hint dependencies in your prompt's `handle` method. The service container will automatically resolve and inject the dependencies when the method is called: -->
コンストラクターの注入に加えて、プロンプトの `handle` メソッドでタイプヒントの依存関係を使用することもできます。サービスコンテナーは、メソッドが呼び出されるときに依存関係を自動的に解決して挿入します。

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
<!-- ### Conditional Prompt Registration -->
### Conditional Prompt Registration

<!-- You may conditionally register prompts at runtime by implementing the `shouldRegister` method in your prompt class. This method allows you to determine whether a prompt should be available based on application state, configuration, or request parameters: -->
プロンプト クラスに `shouldRegister` メソッドを実装することで、実行時にプロンプ​​トを条件付きで登録できます。この方法を使用すると、アプリケーションの状態、構成、または要求パラメーターに基づいてプロンプトを使用可能にするかどうかを決定できます。

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

<!-- When a prompt's `shouldRegister` method returns `false`, it will not appear in the list of available prompts and cannot be invoked by AI clients. -->
プロンプトの `shouldRegister` メソッドが `false` を返す場合、そのプロンプトは使用可能なプロンプトのリストに表示されず、AI クライアントによって呼び出すことはできません。

<a name="prompt-responses"></a>
<!-- ### Prompt Responses -->
### Prompt Responses

<!-- Prompts may return a single `Laravel\Mcp\Response` or an iterable of `Laravel\Mcp\Response` instances. These responses encapsulate the content that will be sent to the AI client: -->
プロンプトは、単一の `Laravel\Mcp\Response` または反復可能な `Laravel\Mcp\Response` インスタンスを返す場合があります。これらの応答は、AI クライアントに送信されるコンテンツをカプセル化します。

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

<!-- You can use the `asAssistant()` method to indicate that a response message should be treated as coming from the AI assistant, while regular messages are treated as user input. -->
`asAssistant()` メソッドを使用すると、通常のメッセージがユーザー入力として扱われる一方で、応答メッセージが AI アシスタントから送信されたものとして扱われる必要があることを示すことができます。

<a name="resources"></a>
<!-- ## Resources -->
## Resources

<!-- [Resources](https://modelcontextprotocol.io/specification/2025-06-18/server/resources) enable your server to expose data and content that AI clients can read and use as context when interacting with language models. They provide a way to share static or dynamic information like documentation, configuration, or any data that helps inform AI responses. -->
[Resources](https://modelcontextprotocol.io/specification/2025-06-18/server/resources) を使用すると、サーバーが AI クライアントが言語モデルと対話するときにコンテキストとして読み取って使用できるデータとコンテンツを公開できるようになります。これらは、ドキュメント、構成、AI 応答の通知に役立つデータなどの静的または動的な情報を共有する方法を提供します。

<a name="creating-resources"></a>
<!-- ## Creating Resources -->
## Creating Resources

<!-- To create a resource, run the `make:mcp-resource` Artisan command: -->
リソースを作成するには、`make:mcp-resource` Artisan コマンドを実行します。

```shell
php artisan make:mcp-resource WeatherGuidelinesResource
```

<!-- After creating a resource, register it in your server's `$resources` property: -->
リソースを作成したら、それをサーバーの `$resources` プロパティに登録します。

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
<!-- #### Resource Name, Title, and Description -->
#### Resource Name, Title, and Description

<!-- By default, the resource's name and title are derived from the class name. For example, `WeatherGuidelinesResource` will have a name of `weather-guidelines` and a title of `Weather Guidelines Resource`. You may customize these values using the `Name` and `Title` attributes: -->
デフォルトでは、リソースの名前とタイトルはクラス名から派生します。たとえば、`WeatherGuidelinesResource` の名前は `weather-guidelines`、タイトルは `Weather Guidelines Resource` になります。これらの値は、`Name` 属性と `Title` 属性を使用してカスタマイズできます。

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

<!-- Resource descriptions are not automatically generated. You should always provide a meaningful description using the `Description` attribute: -->
リソースの説明は自動的には生成されません。常に `Description` 属性を使用して意味のある説明を提供する必要があります。

```php
use Laravel\Mcp\Server\Attributes\Description;

#[Description('Comprehensive guidelines for using the Weather API.')]
class WeatherGuidelinesResource extends Resource
{
    //
}
```

> [!NOTE]
> 説明は、AI モデルがリソースをいつどのように効果的に使用するかを理解するのに役立つため、リソースのメタデータの重要な部分です。

<a name="resource-templates"></a>
<!-- ### Resource Templates -->
### Resource Templates

<!-- [Resource templates](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#resource-templates) enable your server to expose dynamic resources that match URI patterns with variables. Instead of defining a static URI for each resource, you can create a single resource that handles multiple URIs based on a template pattern. -->
[Resource templates](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#resource-templates) を使用すると、サーバーは URI パターンと変数を照合する動的リソースを公開できるようになります。リソースごとに静的 URI を定義する代わりに、テンプレート パターンに基づいて複数の URI を処理する単一のリソースを作成できます。

<a name="creating-resource-templates"></a>
<!-- #### Creating Resource Templates -->
#### Creating Resource Templates

<!-- To create a resource template, implement the `HasUriTemplate` interface on your resource class and define a `uriTemplate` method that returns a `UriTemplate` instance: -->
リソース テンプレートを作成するには、リソース クラスに `HasUriTemplate` インターフェイスを実装し、`UriTemplate` インスタンスを返す `uriTemplate` メソッドを定義します。

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

<!-- When a resource implements the `HasUriTemplate` interface, it will be registered as a resource template rather than a static resource. AI clients can then request resources using URIs that match the template pattern, and the variables from the URI will be automatically extracted and made available in your resource's `handle` method. -->
リソースが `HasUriTemplate` インターフェイスを実装すると、静的リソースではなくリソース テンプレートとして登録されます。 AI クライアントは、テンプレート パターンに一致する URI を使用してリソースをリクエストできるようになり、URI からの変数が自動的に抽出され、リソースの `handle` メソッドで使用できるようになります。

<a name="uri-template-syntax"></a>
<!-- #### URI Template Syntax -->
#### URI Template Syntax

<!-- URI templates use placeholders enclosed in curly braces to define variable segments in the URI: -->
URI テンプレートは、中括弧で囲まれたプレースホルダーを使用して、URI 内の変数セグメントを定義します。

```php
new UriTemplate('file://users/{userId}');
new UriTemplate('file://users/{userId}/files/{fileId}');
new UriTemplate('https://api.example.com/{version}/{resource}/{id}');
```

<a name="accessing-template-variables"></a>
<!-- #### Accessing Template Variables -->
#### Accessing Template Variables

<!-- When a URI matches your resource template, the extracted variables are automatically merged into the request and can be accessed using the `get` method: -->
URI がリソース テンプレートと一致すると、抽出された変数は自動的にリクエストにマージされ、`get` メソッドを使用してアクセスできるようになります。

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

<!-- The `Request` object provides both the extracted variables and the original URI that was requested, giving you full context for processing the resource request. -->
`Request` オブジェクトは、抽出された変数と要求された元の URI の両方を提供し、リソース要求を処理するための完全なコンテキストを提供します。

<a name="resource-uri-and-mime-type"></a>
<!-- ### Resource URI and MIME Type -->
### Resource URI and MIME Type

<!-- Each resource is identified by a unique URI and has an associated MIME type that helps AI clients understand the resource's format. -->
各リソースは一意の URI によって識別され、AI クライアントがリソースの形式を理解するのに役立つ MIME タイプが関連付けられています。

<!-- By default, the resource's URI is generated based on the resource's name, so `WeatherGuidelinesResource` will have a URI of `weather://resources/weather-guidelines`. The default MIME type is `text/plain`. -->
デフォルトでは、リソースの URI はリソース名に基づいて生成されるため、`WeatherGuidelinesResource` の URI は `weather://resources/weather-guidelines` になります。デフォルトの MIME タイプは `text/plain` です。

<!-- You may customize these values using the `Uri` and `MimeType` attributes: -->
これらの値は、`Uri` 属性と `MimeType` 属性を使用してカスタマイズできます。

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

<!-- The URI and MIME type help AI clients determine how to process and interpret the resource content appropriately. -->
URI と MIME タイプは、AI クライアントがリソース コンテンツを適切に処理および解釈する方法を決定するのに役立ちます。

<a name="resource-request"></a>
<!-- ### Resource Request -->
### Resource Request

<!-- Unlike tools and prompts, resources cannot define input schemas or arguments. However, you can still interact with the request object within your resource's `handle` method: -->
ツールやプロンプトとは異なり、リソースは入力スキーマや引数を定義できません。ただし、リソースの `handle` メソッド内で request オブジェクトを扱うことはできます。

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
<!-- ### Resource Dependency Injection -->
### Resource Dependency Injection

<!-- The Laravel [service container](/docs/13.x/container) is used to resolve all resources. As a result, you are able to type-hint any dependencies your resource may need in its constructor. The declared dependencies will automatically be resolved and injected into the resource instance: -->
Laravel [service container](/docs/13.x/container) は、すべてのリソースを解決するために使用されます。その結果、リソースがコンストラクターで必要とする依存関係をタイプヒントで指定できるようになります。宣言された依存関係は自動的に解決され、リソース インスタンスに挿入されます。

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

<!-- In addition to constructor injection, you may also type-hint dependencies in your resource's `handle` method. The service container will automatically resolve and inject the dependencies when the method is called: -->
コンストラクターのインジェクションに加えて、リソースの `handle` メソッドでタイプヒントの依存関係を指定することもできます。サービスコンテナーは、メソッドが呼び出されるときに依存関係を自動的に解決して挿入します。

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
<!-- ### Resource Annotations -->
### Resource Annotations

<!-- You may enhance your resources with [annotations](https://modelcontextprotocol.io/specification/2025-06-18/schema#resourceannotations) to provide additional metadata to AI clients. Annotations are added to resources via attributes: -->
[annotations](https://modelcontextprotocol.io/specification/2025-06-18/schema#resourceannotations) を使用してリソースを拡張し、追加のメタデータを AI クライアントに提供できます。注釈は属性を介してリソースに追加されます。

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

<!-- Available annotations include: -->
利用可能な注釈は次のとおりです。

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| 注釈        | タイプ          | 説明                                                                 |
| ----------------- | ------------- | --------------------------------------------------------------------------- |
| `#[Audience]`     | 役割または配列 | 対象読者 (`Role::User`、`Role::Assistant`、または両方) を指定します。 |
| `#[Priority]`     | フロート         | リソースの重要性を示す 0.0 ～ 1.0 の数値スコア。       |
| `#[LastModified]` | 文字列        | リソースが最後に更新された時間を示す ISO 8601 タイムスタンプ。           |

<!-- </div> -->
</div>

<a name="conditional-resource-registration"></a>
<!-- ### Conditional Resource Registration -->
### Conditional Resource Registration

<!-- You may conditionally register resources at runtime by implementing the `shouldRegister` method in your resource class. This method allows you to determine whether a resource should be available based on application state, configuration, or request parameters: -->
リソース クラスに `shouldRegister` メソッドを実装することで、実行時に条件付きでリソースを登録できます。このメソッドを使用すると、アプリケーションの状態、構成、またはリクエスト パラメーターに基づいてリソースを利用可能にするかどうかを決定できます。

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

<!-- When a resource's `shouldRegister` method returns `false`, it will not appear in the list of available resources and cannot be accessed by AI clients. -->
リソースの `shouldRegister` メソッドが `false` を返すと、そのリソースは使用可能なリソースのリストに表示されず、AI クライアントはアクセスできません。

<a name="resource-responses"></a>
<!-- ### Resource Responses -->
### Resource Responses

<!-- Resources must return an instance of `Laravel\Mcp\Response`. The Response class provides several convenient methods for creating different types of responses: -->
リソースは `Laravel\Mcp\Response` のインスタンスを返す必要があります。 Response クラスには、さまざまな種類の応答を作成するための便利なメソッドがいくつか用意されています。

<!-- For simple text content, use the `text` method: -->
単純なテキスト コンテンツの場合は、`text` メソッドを使用します。

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

<a name="resource-link-responses"></a>
<!-- #### Resource Link Responses -->
#### Resource Link Responses

<!-- To return a resource link, use the `resourceLink` method, providing the URI and name. Unlike an embedded resource, a resource link returns a URI pointer that the AI client fetches independently: -->
リソース リンクを返すには、`resourceLink` メソッドを使用して、URI と名前を指定します。埋め込みリソースとは異なり、リソース リンクは、AI クライアントが独自にフェッチする URI ポインターを返します。

```php
return Response::resourceLink(
    uri: 'file:///data/report.json',
    name: 'monthly-report',
    mimeType: 'application/json',
);
```

<!-- You may also pass a registered resource class or instance, which will automatically inherit the resource's URI, name, title, description, and MIME type: -->
登録されたリソース クラスまたはインスタンスを渡すこともできます。これにより、リソースの URI、名前、タイトル、説明、および MIME タイプが自動的に継承されます。

```php
return Response::resourceLink(new WeatherForecastResource);
```

<a name="resource-blob-responses"></a>
<!-- #### Blob Responses -->
#### Blob Responses

<!-- To return blob content, use the `blob` method, providing the blob content: -->
BLOB コンテンツを返すには、`blob` メソッドを使用して、BLOB コンテンツを指定します。

```php
return Response::blob(file_get_contents(storage_path('weather/radar.png')));
```

<!-- When returning blob content, the MIME type will be determined by your resource's configured MIME type: -->
BLOB コンテンツを返すとき、MIME タイプはリソースに構成されている MIME タイプによって決まります。

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
<!-- #### Error Responses -->
#### Error Responses

<!-- To indicate an error occurred during resource retrieval, use the `error()` method: -->
リソースの取得中にエラーが発生したことを示すには、`error()` メソッドを使用します。

```php
return Response::error('Unable to fetch weather data for the specified location.');
```

<a name="apps"></a>
<!-- ## Apps -->
## Apps

<!-- Laravel MCP supports [MCP Apps](https://modelcontextprotocol.io/extensions/apps/overview), an extension of the Model Context Protocol that allows tools to render interactive HTML applications within sandboxed iframes in supported hosts. This allows you to build dashboards, forms, visualizations, and other rich experiences that go beyond plain text responses. -->
Laravel MCP は、サポートされているホストのサンドボックス iframe 内でツールがインタラクティブな HTML アプリケーションをレンダリングできるようにするモデル コンテキスト プロトコルの拡張機能である [MCP Apps](https://modelcontextprotocol.io/extensions/apps/overview) をサポートしています。これにより、プレーン テキストの応答を超えたダッシュボード、フォーム、ビジュアライゼーション、その他の豊富なエクスペリエンスを構築できます。

<!-- An MCP app consists of two parts working together: -->
MCP アプリは、連携して動作する 2 つの部分で構成されます。

<!--
- An **app resource** that returns the self-contained HTML for your application.
- A **tool** that is linked to the app resource using the `#[RendersApp]` attribute. When the tool is called, the host fetches and renders the linked resource.
-->
- アプリケーションの自己完結型 HTML を返す **アプリ リソース**。
- `#[RendersApp]` 属性を使用してアプリ リソースにリンクされる **ツール**。ツールが呼び出されると、ホストはリンクされたリソースをフェッチしてレンダリングします。

<a name="creating-app-resources"></a>
<!-- ### Creating App Resources -->
### Creating App Resources

<!-- You may create an app resource using the `make:mcp-app-resource` Artisan command: -->
`make:mcp-app-resource` Artisan コマンドを使用してアプリ リソースを作成できます。

```shell
php artisan make:mcp-app-resource WeatherDashboardApp
```

<!-- This command creates two files: a PHP class in `app/Mcp/Resources` and a Blade view in `resources/views/mcp`. The view name is automatically inferred from the class name. For example, `WeatherDashboardApp` maps to `mcp.weather-dashboard-app`: -->
このコマンドは、`app/Mcp/Resources` の PHP クラスと `resources/views/mcp` のBlade ビューの 2 つのファイルを作成します。ビュー名はクラス名から自動的に推測されます。たとえば、`WeatherDashboardApp` は `mcp.weather-dashboard-app` にマップされます。

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Attributes\AppMeta;
use Laravel\Mcp\Server\Attributes\Description;
use Laravel\Mcp\Server\AppResource;

#[Description('An interactive weather dashboard.')]
#[AppMeta]
class WeatherDashboardApp extends AppResource
{
    /**
     * Handle the app resource request.
     */
    public function handle(Request $request): Response
    {
        return Response::view('mcp.weather-dashboard-app', [
            'title' => $this->title(),
        ]);
    }
}
```

<!-- `AppResource` extends the base `Resource` class and automatically configures the `ui://` URI scheme and the `text/html;profile=mcp-app` MIME type required by the MCP Apps specification. Like any other resource, you must register it in your server's `$resources` array. -->
`AppResource` は、基本 `Resource` クラスを拡張し、MCP アプリ仕様で必要な `ui://` URI スキームと `text/html;profile=mcp-app` MIME タイプを自動的に構成します。他のリソースと同様に、サーバーの `$resources` 配列に登録する必要があります。

<!-- The generated Blade view uses the `<x-mcp::app>` component, which renders a complete HTML document with the client-side MCP SDK bundled and ready to use: -->
生成されたBlade ビューは、`<x-mcp::app>` コンポーネントを使用します。これにより、クライアント側 MCP SDK がバンドルされてすぐに使用できる完全な HTML ドキュメントがレンダリングされます。

```blade
<x-mcp::app :title="$title">
    <x-slot:head>
        <script type="module">
        createMcpApp(async (app) => {
            document.getElementById('run-btn').addEventListener('click', async () => {
                const result = await app.callServerTool('get-weather-data', {});
                document.getElementById('output').textContent = result.content[0]?.text ?? '';
            });
        });
        </script>
    </x-slot:head>

    <div id="app">
        <button id="run-btn">Refresh</button>
        <p id="output"></p>
    </div>
</x-mcp::app>
```

<!-- The `createMcpApp` global is provided by the bundled SDK and handles connecting the iframe to the server, applying host theming, and exposing helpers such as `callServerTool`, `sendMessage`, `openLink`, and event callbacks. For the full client-side API, refer to the [MCP Apps specification](https://modelcontextprotocol.io/extensions/apps/overview). -->
`createMcpApp` グローバルはバンドルされた SDK によって提供され、iframe のサーバーへの接続、ホスト テーマの適用、`callServerTool`、`sendMessage`、`openLink` などのヘルパの公開、およびイベント コールバックを処理します。完全なクライアント側 API については、[MCP Apps specification](https://modelcontextprotocol.io/extensions/apps/overview) を参照してください。

<a name="rendering-apps-from-tools"></a>
<!-- ### Rendering Apps From Tools -->
### Rendering Apps From Tools

<!-- To display an app resource, link a tool to it using the `#[RendersApp]` attribute. When the tool is called, Laravel MCP includes the resource's URI in the tool metadata so the host can render the app in a sandboxed iframe: -->
アプリ リソースを表示するには、`#[RendersApp]` 属性を使用してツールをリソースにリンクします。ツールが呼び出されると、Laravel MCP はツールのメタデータにリソースの URI を含めるため、ホストはサンドボックス化された iframe でアプリをレンダリングできます。

```php
<?php

namespace App\Mcp\Tools;

use App\Mcp\Resources\WeatherDashboardApp;
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Attributes\RendersApp;
use Laravel\Mcp\Server\Tool;

#[RendersApp(resource: WeatherDashboardApp::class)]
class ShowWeatherDashboard extends Tool
{
    /**
     * Handle the tool request.
     */
    public function handle(Request $request): Response
    {
        return Response::text('Weather dashboard loaded.');
    }
}
```

<!-- Laravel MCP automatically advertises the `io.modelcontextprotocol/ui` capability whenever any `AppResource` is registered, so no additional server configuration is required. -->
Laravel MCP は、`AppResource` が登録されるたびに、`io.modelcontextprotocol/ui` 機能を自動的にアドバタイズするため、追加のサーバー構成は必要ありません。

<a name="app-tool-visibility"></a>
<!-- ### App Tool Visibility -->
### App Tool Visibility

<!-- Each `#[RendersApp]` tool can limit who may invoke it via the `visibility` argument. This is useful for exposing private, app-only tools that the UI calls to load or refresh data without making those tools visible to the model: -->
各 `#[RendersApp]` ツールは、`visibility` 引数を介してそれを呼び出すことができるユーザーを制限できます。これは、UI がデータをロードまたは更新するために呼び出すプライベートなアプリ専用ツールを、モデルに表示せずに公開する場合に便利です。

```php
use Laravel\Mcp\Server\Attributes\RendersApp;
use Laravel\Mcp\Server\Ui\Enums\Visibility;

#[RendersApp(resource: WeatherDashboardApp::class, visibility: [Visibility::App])]
class GetWeatherData extends Tool
{
    // ...
}
```

<!-- The `Visibility` enum has two cases, `Model` and `App`, and defaults to both. Use `[Visibility::App]` for backend actions the UI calls directly, or `[Visibility::Model]` to make a tool unavailable to the UI. -->
`Visibility` 列挙型には、`Model` と `App` の 2 つのケースがあり、デフォルトは両方です。 UI が直接呼び出すバックエンド アクションには `[Visibility::App]` を使用し、UI でツールを使用できないようにするには `[Visibility::Model]` を使用します。

<a name="app-configuration"></a>
<!-- ### App Configuration -->
### App Configuration

<!-- The `#[AppMeta]` attribute on your app resource configures the iframe's Content Security Policy, browser permissions, and any library scripts that should be included in the view's `<head>`: -->
アプリ リソースの `#[AppMeta]` 属性は、iframe のコンテンツ セキュリティ ポリシー、ブラウザーのアクセス許可、およびビューの `<head>` に含める必要があるライブラリ スクリプトを構成します。

```php
use Laravel\Mcp\Server\Attributes\AppMeta;
use Laravel\Mcp\Server\Ui\Enums\Library;
use Laravel\Mcp\Server\Ui\Enums\Permission;

#[AppMeta(
    connectDomains: ['https://api.weather.com'],
    permissions: [Permission::Geolocation],
    libraries: [Library::Tailwind, Library::Alpine],
)]
class WeatherDashboardApp extends AppResource
{
    // ...
}
```

<!-- The `Library` enum includes pre-configured CDN scripts for common front-end libraries, such as `Library::Tailwind` and `Library::Alpine`, and their CDN origins are automatically merged into the CSP. The `Permission` enum covers browser permissions such as `Camera`, `Microphone`, `Geolocation`, and `ClipboardWrite`. -->
`Library` 列挙には、`Library::Tailwind` や `Library::Alpine` などの一般的なフロントエンド ライブラリ用の事前構成された CDN スクリプトが含まれており、それらの CDN オリジンは自動的に CSP にマージされます。 `Permission` 列挙型は、`Camera`、`Microphone`、`Geolocation`、`ClipboardWrite` などのブラウザー権限をカバーします。

<!-- For computed or dynamic configuration, override the `appMeta` method on your resource using the fluent `AppMeta`, `Csp`, and `Permissions` builders from the `Laravel\Mcp\Server\Ui` namespace. -->
計算構成または動的構成の場合は、`Laravel\Mcp\Server\Ui` 名前空間の流暢な `AppMeta`、`Csp`、および `Permissions` ビルダを使用して、リソースの `appMeta` メソッドをオーバーライドします。

<a name="building-apps-with-boost"></a>
<!-- ### Building Apps With Boost -->
### Building Apps With Boost

<!-- Laravel MCP includes a dedicated [Boost](/docs/13.x/boost) skill reference for building MCP Apps. If you have [Laravel Boost](/docs/13.x/boost) installed, your AI coding agent can invoke the `mcp-development` skill and ask it to scaffold an app resource, Blade view, and linked tool for you. -->
Laravel MCP には、MCP アプリを構築するための専用の [Boost](/docs/13.x/boost) スキル リファレンスが含まれています。 [Laravel Boost](/docs/13.x/boost) がインストールされている場合、AI コーディング エージェントは `mcp-development` スキルを呼び出し、アプリ リソース、Blade ビュー、およびリンクされたツールをスキャフォールディングするように依頼できます。

<!-- For the complete protocol reference, including the full client-side API and schema details, see the official [MCP Apps documentation](https://modelcontextprotocol.io/extensions/apps/overview). -->
完全なクライアント側 API とスキーマの詳細を含む完全なプロトコル リファレンスについては、公式 [MCP Apps documentation](https://modelcontextprotocol.io/extensions/apps/overview) を参照してください。

<a name="metadata"></a>
<!-- ## Metadata -->
## Metadata

<!-- Laravel MCP also supports the `_meta` field as defined in the [MCP specification](https://modelcontextprotocol.io/specification/2025-06-18/basic#meta), which is required by certain MCP clients or integrations. Metadata can be applied to all MCP primitives, including tools, resources, and prompts, as well as their responses. -->
Laravel MCP は、特定の MCP クライアントまたは統合で必要な [MCP specification](https://modelcontextprotocol.io/specification/2025-06-18/basic#meta) で定義されている `_meta` フィールドもサポートしています。メタデータは、ツール、リソース、プロンプトとその応答を含むすべての MCP プリミティブに適用できます。

<!-- You can attach metadata to individual response content using the `withMeta` method: -->
`withMeta` メソッドを使用して、個々の応答コンテンツにメタデータを添付できます。

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

<!-- For result-level metadata that applies to the entire response envelope, wrap your responses with `Response::make` and call `withMeta` on the returned response factory instance: -->
応答エンベロープ全体に適用される結果レベルのメタデータの場合、応答を `Response::make` でラップし、返された応答ファクトリ インスタンスで `withMeta` を呼び出します。

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

<!-- To attach metadata to a tool, resource, or prompt itself, define a `$meta` property on the class: -->
メタデータをツール、リソース、またはプロンプト自体に添付するには、クラスで `$meta` プロパティを定義します。

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

<a name="icons"></a>
<!-- ## Icons -->
## Icons

<!-- MCP clients can display icons for your server and its primitives. You may declare icons on a server, tool, resource, or prompt using the `Icon` attribute: -->
MCP クライアントは、サーバーとそのプリミティブのアイコンを表示できます。`Icon` 属性を使用して、サーバー、ツール、リソース、またはプロンプトにアイコンを宣言できます。

```php
use Laravel\Mcp\Enums\IconTheme;
use Laravel\Mcp\Server\Attributes\Icon;

#[Icon('mcp/server.png', mimeType: 'image/png', sizes: ['48x48'])]
#[Icon('mcp/server-dark.svg', theme: IconTheme::Dark)]
class WeatherServer extends Server
{
    // ...
}
```

<!-- The `Icon` attribute is repeatable, so you may declare multiple icons to provide different sizes or light and dark theme variants. -->
`Icon` 属性は繰り返し指定できるため、複数のアイコンを宣言して、異なるサイズやライト・ダークテーマのバリエーションを提供できます。

<!-- Alternatively, you may define icons programmatically by overriding the `icons` method, which is useful when an icon depends on runtime conditions: -->
あるいは、`icons` メソッドをオーバーライドしてアイコンをプログラムで定義することもできます。これは、アイコンが実行時の条件に依存する場合に便利です。

```php
use Laravel\Mcp\Schema\Icon;

class CurrentWeatherTool extends Tool
{
    /**
     * Get the tool's icons.
     *
     * @return array<int, Icon>
     */
    public function icons(): array
    {
        return [
            Icon::from('mcp/tool.png', mimeType: 'image/png'),
        ];
    }
}
```

<!-- Icons defined via the attribute and the `icons` method are combined automatically. Icon paths are resolved as follows: -->
属性で定義したアイコンと `icons` メソッドで定義したアイコンは自動的に統合されます。アイコンのパスは次のように解決されます。

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- Paths with a URI scheme, such as `https:` or `data:`, are used as-is.
- Relative paths are resolved to a URL using Laravel's `asset` helper.
-->
- `https:` や `data:` などの URI スキームを持つパスは、そのまま使用されます。
- 相対パスは、Laravel の `asset` ヘルパを使用して URL に解決されます。

<!-- </div> -->
</div>

<a name="authentication"></a>
<!-- ## Authentication -->
## Authentication

<!-- Just like routes, you can authenticate web MCP servers with middleware. Adding authentication to your MCP server will require a user to authenticate before using any capability of the server. -->
ルートと同様に、ミドルウェアを使用して Web MCP サーバーを認証できます。 MCP サーバーに認証を追加すると、ユーザーはサーバーの機能を使用する前に認証する必要があります。

<!-- There are two ways to authenticate access to your MCP server: simple, token based authentication via [Laravel Sanctum](/docs/13.x/sanctum) or any token which is passed via the `Authorization` HTTP header. Or, you may authenticate via OAuth using [Laravel Passport](/docs/13.x/passport). -->
MCP サーバーへのアクセスを認証するには 2 つの方法があります。[Laravel Sanctum](/docs/13.x/sanctum) を介した単純なトークン ベースの認証、または `Authorization` HTTP ヘッダーを介して渡されるトークンです。または、[Laravel Passport](/docs/13.x/passport) を使用して OAuth 経由で認証することもできます。

<a name="oauth"></a>
<!-- ### OAuth 2.1 -->
### OAuth 2.1

<!-- The most robust way to protect your web-based MCP servers is with OAuth using [Laravel Passport](/docs/13.x/passport). -->
Web ベースの MCP サーバーを保護する最も堅牢な方法は、[Laravel Passport](/docs/13.x/passport) を使用した OAuth を使用することです。

<!-- When authenticating your MCP server via OAuth, invoke the `Mcp::oauthRoutes` method in your `routes/ai.php` file to register the required OAuth2 discovery and client registration routes. Then, apply Passport's `auth:api` middleware to your `Mcp::web` route in your `routes/ai.php` file: -->
OAuth 経由で MCP サーバーを認証する場合、`routes/ai.php` ファイル内の `Mcp::oauthRoutes` メソッドを呼び出して、必要な OAuth2 検出ルートとクライアント登録ルートを登録します。次に、Passport の `auth:api` ミドルウェアを `routes/ai.php` ファイル内の `Mcp::web` ルートに適用します。

```php
use App\Mcp\Servers\WeatherExample;
use Laravel\Mcp\Facades\Mcp;

Mcp::oauthRoutes();

Mcp::web('/mcp/weather', WeatherExample::class)
    ->middleware('auth:api');
```

<!-- #### New Passport Installation -->
#### New Passport Installation

<!-- If your application is not already using Laravel Passport, follow Passport's  [installation and deployment guide](/docs/13.x/passport#installation) to add Passport to your application. You should have an `OAuthenticatable` model, new authentication guard, and passport keys before moving on. -->
アプリケーションがまだ Laravel Passport を使用していない場合は、Passport の [installation and deployment guide](/docs/13.x/passport#installation) に従って、Passport をアプリケーションに追加します。次に進む前に、`OAuthenticatable` モデル、新しい認証ガード、およびPassport キーを用意する必要があります。

<!-- Next, you should publish Laravel MCP's provided Passport authorization view: -->
次に、Laravel MCP が提供する Passport 認可ビューを公開する必要があります。

```shell
php artisan vendor:publish --tag=mcp-views
```

<!-- Then, instruct Passport to use this view using the `Passport::authorizationView` method. Typically, this method should be invoked in the `boot` method of your application's `AppServiceProvider`: -->
次に、`Passport::authorizationView` メソッドを使用して、このビューを使用するように Passport に指示します。通常、このメソッドはアプリケーションの `AppServiceProvider` の `boot` メソッドで呼び出す必要があります。

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

<!-- This view will be displayed to the end-user during authentication to reject or approve the AI agent's authentication attempt. -->
このビューは、AI エージェントの認証試行を拒否または承認するための認証中にエンドユーザーに表示されます。

<!-- ![Authorization screen example](data:image/png;base64,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) -->
![認可画面例](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABOAAAAROCAMAAABKc73cAAAA81BMVEX////7+/v4+PgXFxfl5eUKCgr9/f1zc3P29vby8vLs7Ozj4+Pp6env7++RkZF5eXlRUVF9fX2Li4uEhISOjo4bGxt0dHS0tLTd3d12dnbLy8vW1tapqanFxcVMTEygoKDDw8PIyMgODg7BwcGwsLASEhKbm5uBgYFGRkbh4eHf398gICCXl5fS0tLR0dG6urolJSXPz8+Tk5MVFRVbW1va2tq4uLijo6NnZ2eZmZnNzc02NjZWVlaIiIhAQEClpaUuLi6enp6Hh4e2trZsbGzY2NjU1NStra28vLwyMjJjY2MpKSmVlZVfX187Ozu+vr5OTk7PbglOAABlU0lEQVR42uzBgQAAAACAoP2pF6kCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGB27Ci3QRiIoqiNkGWQvf/tFlNKE5VG+R1yjncwUq5eAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwilAKIn325Y8zwv1VO7NuplvEFEqSeNeOeKWgYDKJkncy7zlwwSEkQ8S958zb3Xprc1AIK31peaNb3FXyjCG27LOQEjrMknclZKOvLX9SjW7DwRSct23SdsTp3DPjvlW2zhQTkBAeQyUVhXucr9NfeQtAWGNxPVJ4f7ut2ndLuMmEFrp87wq3IOSfvpmvkF4i8I9OfdbTUB49btwArcrafSt6xvcxFa4rnCP+23x/xRuY/yeFe53wNU29wTcRJ9bFbhzwG3n+PhLwH18sW8HNw4CURQEsYXQgMb5p7uGFQ6iqQrBh9b7jLxNR+pvwL3HdKBCyb7O8Ra4a8CNzzoXIGSuH0eqAQdNJtzpfkL1/1NIef0/pD47cPeFeixAyuFGvRbcexwuVKjZ1+PxN+p2Bm6f/sQANWOdu8C9XsMnOOg5P8KNh3+EuwP35N8AkjaB2+7ALUDMN3APf2XYFoGDKIG73hgEDoq+gXv4M+q2CBxECZwFB1kCZ8FBlsBZcJAlcBYcZAmcBQdZAmfBQZbAWXCQJXAWHGQJnAUHWQJnwUGWwFlwkCVwFhxkCZwFB1kCZ8FBlsBZcJAlcBYcZAmcBQdZAmfBQZbAWXCQJXAWHGQJnAUHWQJnwUGWwFlwkCVwFhxkCZwFB1kCZ8FBlsBZcJAlcBYcZAmcBQdZAmfBQZbAWXCQJXAWHGQJnAUHWQJnwUGWwFlwkCVwFhz8sXcHOWoDURRFLXkDX39e+99mQMhtKRBIRUSCV+eMuxlevbILEUvgLDiIJXAWHMQSOAtuNWP0xiIEzoJby6j9QuIWIXAW3FLGpW4Ktw6Bs+BW0pe2SdxCBM6CW8f1eKpwSxE4C24Z1+Opwq1F4Cy4VVyPpxK3GIGz4NZwPZ4q3HIEzoJbwS1vErccgbPg8t3yJnELEjgLLt1d3uoucRqXSuAsuGgPxltt437F9dgIJHAWXKoxqv50Iu39XolcHoGz4LKMm67aH6lx3Bl5qLp7XGldBoGz4GKM2l/p36/FefuQTeAsuBSvi1Vj7u/3jS8ncBZcitd5m05ibXw3gbPgQvRM3g5twmUTOAsuRM/k7dRP/8+7hi8ncBZciJqs26kFLpbAWXAh5ut2Gl0ewkUSOAsuw3hQp6mru90lcHEEzoLL0GfW6nZd958y2RdV5S1DCIGz4DL0W6/nlodwGQTOgstwJunzPo0JAmfB8SRJ2zsMX9fKIHAWXIZd4BA4Cy7VUaQSOATOgksjcAicBRfrzYFzES6DwFlwGX6K9JEfx98SuM2C48mZUuAQOAsuzLDgEDgLLpaXDAicBRdL4BA4Cy6Wi74InAUXq44kfeBX95khcBYc/ztwvmyfQeAsuAz1kySBQ+AsuDAtcAicBZfqTNLnHXiZIHAWHM9u+n7eO1kmCNxmwfEgcAcvURE4Cy7N+ZZB4BA4Cy7MOwPnh59TCJwFF+J8COcRHAJnwYUZ+8EJ9Rf7dpCbQAwEUXTRF7B63/e/ZqREgEiIgBlW5feWHOCrbDMInAWX5nZGFTgEzoILcw3ccgWHwFlwYeZTXWpXcDEEzoJLMfWhCVdOqDEEzoKLsT6zvFrgcgicBRdj6mIMOATOggtze2Yw4BA4Cy7M1MV4YkDgLLgwtwlnwCFwFlyYOV+nMuCSCJwFl6SuxoBD4Cy4LH3yv3BtwGUROAsuyjq3wMqAyyJwFlyUqas5NwBJIHAWXJYzjerymX0YgbPgwqzDhWsH1DgCZ8GFmTpYuCkH1DgCZ8GlOTjEphxQ8wicBRdnHSpcOaAGEjgLLs4cadVyQE0kcBZcnn67cLMcUCMJnAUX6N3CTelbJoGz4BL1W8VqfUslcBZcpK7XR9wqDwypBM6Cy/RytUbfggmcBRfqrlur/596+hZM4Cy4VOs+XfP4dUHfogmcBRern9Vrlr6FEzgLLlfXvf6bN++n2QTOggvW9Uv3tW4/efP9QjaBs+CSzaoHjZvvnx1PNyBwFly2rkf0bRMCZ8GF63puuX4LJXAWXLyWt20JnAW3gfvEeTzdh8BZcFtol29bEjgLbg/d8rYhgbPgdjHt7m07AmfBbWRa3fYicBbcXqa/6yZvexA4Cw5iCZwFB7EEzoKDWAJnwUEsgbPgIJbAWXAQS+AsOIglcBYcxBI4C44vduuABAAAAEDQ/9f9CB0RsSVwDg62BM7BwZbAOTjYEjgHB1sC5+BgS+AcHGwJnIODLYFzcLAlcA4OtgTOwcGWwDk42BI4BwdbAufgYEvgHBxsCZyDgy2Bc3CwJXAODrYEzsHBlsA5ONgSOAcHWwLn4GBL4BwcbAmcg4MtgXNwsCVwsVu3LQlDYRzGb8t7PaeVUVmtmkIPRlpKBor1IiSh7/95ysUEdVOnFoe76/dWlJ3juPiz4ACzCBwLDjCLwLHgALMIHAsOMIvAseAAswgcCw4wi8Cx4ACzCBwLDjCLwLHgALMIHAsOMIvAseAAswgcCw4wi8Cx4ACzCBwLDjCLwLHgALMIHAsOMIvAseAAswgcCw4wi8Cx4ACzCJyrC67/VOv9/2YJvxSSZcnlQ2VZypN9HzITQxyS/gK9zEDaT29LZ0/Xu2elYy/pWxFPZuGdVpuF68/yVXbSsR7zoYZYQ+BcXXD7+sOXRRU09CBL0tHQrizM10Qb4o689q3Od7CsjLnRgWMZcrXX00jtpDjlsiot/+TckwlWjt5rGmnt3yW+F1UN1cUaAufqgove9CBL4FJzKHD3MmozSAjcZUeHvZWnX1Yll3hVXrOmw266BO6/cXTBFTVSkDlsfRA4NwLny6imxgbutq3jGtvTL6tWlViXPR0THKz8ReAyz9viBgLn6IJb00hL0lp/9bVB4NwIXLAjI9qxgStWNM5haYbLepIYF4HGaWV/PXDdXEW74gYC5+aCyxzqwKOkUnqpqxK4L/bOtC11HAzDL8tbKYK4VRBxoYCDLHPAgiIoouKCiMf//2tmSE3atClQcK7p0dwfZjxasAnN7dNsDYrg8BJ41JJIcM8lFGNk51cWpsGJkkIPRvH/VHDx83dElIILDMFMcGm02PcX3xDxDxPcfs1NkIZRVxPcNfAUUSC4Aotbg5vnbuLp+WaTZbhH7j13apT7175OLXgGDu6RUn5LPyWyt1s9/KSv/peC20KUggsSwUxwLZwyIv+thoIluPtXwsWXCS4DwWZZwZlKKcWAY2Jqhyv6epXKJ81a4mEfTcYxz8qql9EkBTwX+Mmk6R5yaLmvi6dXwlAK7tsRyARnDrSVnpDwECzBUaTg5hTsw1RUEeyEIuRPV8de9BB12WsILJQ3NNmdUVkTJGi8Rc80JOhX3KUxQZO853UhBfftCGSCu/q8uSnjlIkUnG8CIbhd01rAYDeDf3GCO0aTHeDZR0Ik6V1ZyYaoF+4VCSVHyg73kVCWgvs5BDLBmRdi7lN0JVUKzi+BEFzbfGEIbAxxStMuuNAYCZvgIHSEhNSMytoSDKS2dY9u0mgVCRdScD+GICY4s2EYMUjoOOXu6wQXbv86zTVjoopIdIu1y5dHb5uGD4q1NPhDfbq4O72oJ/8rwSXr6atcPqp4n0C9WHvg1j0lm89XFxXF6w2bxdpzNi4QnKC2frdjswQHI5zyYn8dUcwYmOCsAGesg5MKEsYzKusWCfuCAPce8pqD97qQ4GLtwm2tmI2CJ4ls7uplXZGCCzBBTHB/4ZQJu6rLNslohDWw2NcICWhO/1dCE81E4S7k9rCEhMEt8DxuVdmw27EKjKZGKADEbkjvEcCbRngCgBdNxC8ml9N39qa3Mb+CyzQ0wiUwbjRCOQyEZiuCJqVeTgETdoLTg+oT3fz5JEFvEY+QYEyi7jIqxT6a9J9DMwRX2Wmgid56UbwFZ7b2IVjkccoeJ7h372HpHhLOvCsrj65uDFVHQtercxfHLsGZdT0BRqi4qaPJYJdWHjvwfnrEbQ8JRsusysn0J8hdf9uwDFJw3zvBKQ3WrXKMhIolOCR0XDc9GIUsurELLtxBi6MMWByU0Y6RCjtWVPxiE1G5hvEwa1ZWeK+ENiKnfhPcHRIiZ+xkdPP0HmHKyQfa6V04ImsMYhPnr2/37N9RHGWsD9Bi3PUSXHQT7YwPPQXXxSlVBRgpnFKwCy6OJglws4OEnHdl5ZCw556IMgIBZSREnYIrOaa03FXRhj4MA4EeuAVQaCAjcqXQeuL5C5ZACu6bJ7gCTiEJJGk26fuvEFySt1g1DpS7Ejp4bzsEl6miT8FleuhgovoSHLvVKitAUAdIyLGWzbPhEFyyj3YuAfIa2qnxZcxqvOYfxIL7pSGPvuElODAlkAcGKYIWYoKzClIGAXWNkPKurL/c8W9IhywEXGmE9GzBqRPXBZFxCC6no517KbiAEsAE16EOY+t6Bl8guLxTOK+8R3iM31zjTw/Qp+BODHTxHvYlOGa0c66gazDlQkcnpQNOcMkRckSieYfIjXV7Ge8Mp7geRILbQDdrXoJbc8xSq9NPjwmOfVlbakQmPHKPoo4X6wbzFlxigC60DCe4nLPuH6XggknwElzMbGi/7Tklv7rg3Jffb3qhMyKWNbQze+OfoA/B/QKARJVaYjSZjHQqAmGbvc07oW3zqcRaD0DRbsmDEpVma3g9ol+H7AXaRwfsOMa1vYwjdNJQ3YL7zZp0v7M5xk+KQsHRMD5w3HKmOcGVkXC4lOC2kBBRgRFCgq4sKzilzCrgutM3kNW7dWBHQwdlRQoukAQvweXs6xdUA6cMFxGc+vAvz0goPZhwAjM6hWgoU+zRCMevErouViCWrbFJ9WHW+BlGw+AaRuLBBm0WmwpAqIwE/TxGSjGk4W6xtah9tmLcMldCM8VbsfVlYStjxrkGEp4dxta2mqr6d0pHhrGWj4cPdg0k6CFHGV9zj7G/L1lLHToFxyZaVH+Rl1bKtJ9QLLiQxoepnjk8zgluQL/0Lzh1S3evZEggoQHLCu4vNOnESQO5Muy/o4SU3tVjTM2yyq1A9uFfRkjYfiC0wT9ScN88wR1xYadFO+TmC857mohJpAuE0PWnNsg/Gkgw7mj7+ECTXb7xV8+7cQBuVJbjRUfCOAkAp86O+jQSej4FB6+0i0f54JZ1jM0GqXDTZ3GHL3Cj4lzZqzWB0NSR8MiVMUKDWI0243Wn4CZIOEo4FrXviQUHHa4PNUM/G7vgNCSoiwkufUA5Od5q0DRZAYs6Et6XFdwjEgw20P7Z/6onOMG9KkDI60h4kNNEAkngElyUv2MpIqG4uuAMdp+7XjK/odjuMgtAUTaRMFbsjT+lzp44XNGQYNRtMx8OXWuKmj4Fp5qJQO++IWELCPUIIe/od2pxBW5k2C/iFW8JpmgXnM5aJauVc05wbJqFZtkoPKZ/gdyCY27tcf13OU5woQXXuR+hNzlgsJvozWUFt4+EG2CcImHDLrhJyLGz164UXCAJXILbZXYhxCL00ltVcCeuDUHWraGviWAi/Iut8R/NWRkRe0eTWxKQ3G2sotNg6ktwcGCgjXIIxJj5bsQVuO0casQX5xSUDbvghu7pFGWH4Dbcm5DmqCoFgmMdqhXbu+oqJzhFp11mvgUn7uk6QcLRkoILa2Zgt/fqDaimmeCOQgB8eu5IwQWSwCW4kRmYHDdpenxVwRnu+RdtFklK62AjxaTHGn9ljuBe0X6rtoeErrtcA5+C4zfArUZnb7+i20+w4X4PYLy4b8MN+5t30STJC65nnkYMLOLUjkLBQcsSKSSoebhb1CoS4ssKzjgFjkckjJYUXNGmfkdIi1qCK7iWW0yk4AJJ0BJc03krd4GE2mqC41+yzwR3SI0iyAA9m+BgtuBqXMKijXE9auPdqVl22EnUSZx3J0UvgIDEyXHqGk3sJ7jHpyzeriduwZWBYWmnbhMcS1ujqB2aVsWCu6XvzWLjqUNwIyQcLCm4zTOgcMatLim4GyQUozZSSMhaglOAoUrBBZmgJbg9vimygbj3VQV3KhRcjr6foBtQsxp/b7bgDnUkNBJ0OqsnSd9rUWMj/OQGHCSLe/0IMnjB5YTT/b0F1xFt6/nCCS6KnvQ8BJfUrWUKH/SDEk0TKSwhOK18lQAeZmEMLSe4IXpSZAdWQQruDyFgCS5URULEAk0eVxRcViA49sNt4DCQEGONf3+W4NjcCT3PXu/Jk2/BwQGbf8KLb7eHFJHgmi7B3c4U3LZoo7VbTnBZ9EQTCo59fcfWiPbBIbg9JOwsJrhcltKMeiisR425lOA20ZM3duCHFNyfQsASXBq92FpRcH8LBZcSPDiAJbAz1qTPZwku3EeTK3bJe9P1L7gmqwEbSq6BboQnyASXmym4WxD0Q75xgntATwwvwV2ZcmZnsesU3AWNgAIyDULH19YrbOaKgFyDcOwtuHf0ZMM6UAruTyFgCa6FXjQUD8F1VhHchnAnCw0J4cUEN0R2UvMTXMa34JJjZAGRoVwjQx9db32B4HZFCS63aIJreAkuyvb0a9FK5wWn6t7VsI2EDV+C+80uGDcfSGguleCOpeD+PIKV4JIl9KTgIbj3VQT3LNrTP0y7qRcS3DGavMecCTAlIOxLcLzKGknnNhvY33rIhACgtbrghqI+uAInuAR6FuxNIDh+99KYQQc3ecHBkeAz4D/bui/BhQ0kXHhul6Qpc/vgOik3j1Jwfx7BSnCn6E3HQ3C4iuDyomnvBfrNRQTXLdHFq84GbnzJjr7baHGt8LM8RnkgfIngjkSjqI+iUdTNBXf0tddX6/P+9i+34NJI0OseO59iVfElOEjRp9V47UDVmj+K2gUBUnB/HsFKcH1hQkCCEaOC4y6wx5UElxTdHw1ZpJkvuHgDCfqL6P1XF1xBF+2I1HE6dXN1wUXiQGHf01XRPLhGyIfg6P7MYfOcm27Bwbt4B17WubkH/gSXKHlkwrMqEoqegmO6PZWC+x4EKsG1ac82z5bVPkOuWZwdXnBKiYaMhQQHLXckXDeQkF9AcKEyCsYg/0bCZFXBsQHaQbzHdcONnBbH1QWHe+5T+wBecOdIuPMhOHqyaY2kKhAILs0/VIvRoeb1KTjYR6Gl1B6d9egpODaOPw4vJ7htOmYfDKTgApXg/qKrmnnqttZWNQ9h2eUGqeD4FQOLCu43mvxyrUXtwQKCS6FJy6PviKG2Nqdk/QiOPVBPz8JTyVrKDzHnuq/CVwhObzuXH+GleC1qIwaMLinXtSoQHPepDqhEOcHx3YxHKlgoN2z6n1/BsXGZLcVuIvprDj0Fx48fM/ZJGY8XEdwzHZIOBlJwQUpwythjFaHZOPQoUwfrjbpCp+CukfCyoOCUARKMNJjEWmhytYDgcmgyUoV9PT2mDOXVbOUhf4Lbpx5iv/ba1qbeFTB51L5CcKg9gMlxCQl60mM3kZbq2A1gOCPBddGiIBIcJAdoMrhjwemlh0ht6ldwrGMUy+wPV+i0iiathXYT0S6AH0bSK4sIromEckCMIgUXpAR34nUDtIOEDVtk6h+qoJ5MkBecdUD1VAVQunMFx7a70SdNBUC9G9A0ocwX3JOBJsd5Gxlrz0TjWCGNq3tEN2wTCG7t3I3p52d2KtZbbtiHac3d5nYiuJrgGJ3ndugg1+JWsXOCS1S5BzGoFwO6ltdbcNBASjUkFBzUS+yIrdvD9Xpu54hZ9wD8Cw7ukNLbfu5G88epEX7yrnoLjhuh3jPN2t5HlpfnC05Fk+snBSD+vz8RUgouSAmuQ2ODk0frpvEAGYZ5+BovuF9I0Ro6KnMFBxtIKQ2qSGkkYL7gjlBExyYCNPqdvX6JWlnhPTBnyLhtmOUwi1b5LG/WClJYvV6b9A1kqCsIboxORuEZO/pq5b1ODz9JwSzB7XHFEgkODjUUY+SXe8ZiTUcxg/jCO/rqo0nqQ2M7vi8kOOgjfXUjInf0/f8JUIKLRTwnIfSsi3GCPKk7XnBwjRaLCA5e0U3kEBYQXN9bTgXRMxni4Edw6ggJDyyVsG64glMDu0iorCC4LadjSlnRMxl2RWerzBScdbZpL8FBZoAiIi/LPkT2whD77WzJZzJ0YTHBdeWW5YEiQAmONUM3u1ZQUMe83xSn4Coln4KDWknwEKUVBQftHjroJ8GX4CbOBzlsWt1w92hHfy4i4XAFwZ3n+Wqo5sVP1XrQ0MFQgZmCC2nUwzFPwUFyqKOLVnT5p2QflNGF/lcY5gsO1JbLb3VYUHAwlIILEgFKcB9mI1DBTcXWhbP+jozSOYBTcPB74FNw0ORlVNoPw8qCgxjfYo19FXwJ7goJvTBQEhrrhlOGaBEpwBM9zxUEBw8RtOhlQCw4OOPN0agpMFtw0KG+AoHgGAebyDMu+hiREfAwQp5yfd5ie0pN40XbhoUFp67pUnDBITgJLqrTRiCgb1t9E94dIyGylQCX4MgBEWqVOYJjZIcRlt5qSYBVBUeIb7AWpt0nAXwJLquzZwEyntHqhnuiOmjcJwDC5tGvKwkOkmy44uNCmfFk+8dUlfXTXYYA5gkujSY5seAYT9t9y5v7WYDVBAehwv7ANtpQAVhUcBDLMY2XOu2F5sEx6uylu7AEUnDfNMEtjpLPbe8WmzHvA6KHl/e7d4UwLEz48eX4fuM5/7UVcXaY293O5aMKfD3xbO7mvNgNwUrwEo/V0xs3t4eJuepoFy5vNorNJHwxicNibef8+TDzVTWWKeQ2dq7S2aj/+u0W3+6PC5UlKjh2kN7YecudwXJIwX3HBCf5n2CCk3w7pOD+yAQnkYKTSMHJBCeRgvvRSMHJBPfjkYL7vkjByQT345GC+75IwckE9+ORgvu+SMHJBPfjkYL7vkjByQT345GC+75IwckE9+ORgvu+SMHJBPfjeeoRgrIJrUQKTiY4iUQiBScTnETyg5GCkwlOIvm2SMHJBCeRfFuk4GSC+4e9821NHIvC+EkJeUxqDEkkMVbpSEVRasWCioKIFmtfFPr9v82ae73XZE2z3e0fdpzze2Mnc3NyTpn8eK4ahmEuFhYcJziGuVhYcJzgGOZiYcFxgmOYi4UFxwmOYS4WFhwnOIa5WFhwnOAY5mJhwXGCY5iLhQXHCY5hLhYWHCc4hrlYWHCc4BjmYmHBcYJjmIuFBccJjmEuFhYcJziGuVhYcJzgGOZiYcFxgiunYv6dCtGVaRpn/5Kq9LU4pitexLX+FbZo8tPoqcS8qiWBOviJ0fJYacuMgAXHCe7n6ODvLIluAJPyJNjS11LDLR1YAC79O16AJn0ePZWYV7UkUAc/MVoeA/hFjIAFxwmujD9XcO5FC84lhgXHCe6LsQxJDa+GxCq8tzeLFtF3CO5psbDpIwzvE5JMFospfRI91f9EcM1gQQwLjhPcN1HD/Sfv7c9boJwxEvoG/ieCuwcLjgXHCS4LC44F96fDguMEx4JjwV0sLDhOcP9VcE438Pzai0GCbu+FBNPNNvFr4yvKYse1frJdTEhw3etZ1Jgf1j02DRI0e10ylvf9KNxM8xZo9uYkqbzUfX/xZNIRc133veD2WrxT1+sB6B14E/UdEljPaTf1J5dUl02yJotDL7eijD48O67f9I7HR721nKpccEM9hcR46IWHC77YlMP49Rom/ccX4zTa1V3NT1atal5wxRU2erobOnDVfuxH/cf2FTEsOE5w3yO4TgLBys6FkhYkvkkn1Fr0rOPphlpXl6fHqNl1SNZGtmIMnwRVH4JkSSmWqhCNxWetinkmWxnqcHKjpojtGgTRHWme4FuUsgNiEmywlj2UCi7OT0FOAEnfoQzXfUhC/cuqhhBEv7Tg3q+QQNEmIjfML6mF4ZAYFhwnuC8UXBd+q2k+b4BNLm8B+xu78eSjXzktjxDEO7dxC7SPp7cQ3k0H7UdgaxwFF+C1M5i+hcC6SHBuH/3uztn1gDt5HPdvA2dUR2QS7TqdEOgcaJx8ZG2A1sgZtkN4jWPN7hav48bwzkc0IMUAGCg9b0mc6mFSJrjiKRwfUevZOVRXKtOt7yfOIE4wP7ax6KO1NJ9jD+gowb1fodnpQE5XJbK38GY7ZzfzsBVL+sCUGBYcJ7gvFBxCGR/mgJO59zfHW3gCNEnxippx/CFQp/eE/6wYiI+6wpMlNqL3wM254OwVfJfkAc8gMhJ0Saz3sc+9B6d9ZM3hjeSaHryBrAk8UYoZYU0Kq4+xePVxVFkDyVWJ4IqnsGrwbqTSVggMUszgO8cfYMs6qjMzhGdrwRVXyL8HVwmwrcpIu0VQYcGx4DjBfYfgHBIMgVHm3g/QIkG87tARI1iNSNBGYsnTvQoJrDo8QwrukSSuh8W54J6QNEhghak7B6uVS4I57osFNwVmRMqCj7ImuiRZICBNS/71FKtbKcAZFlQmuIIpxJExSZ6BESnWq5gEVaAh6gjNCkbAixZccYW84GZKZ3rA6c0NP+bFguME95WC03awgV+Ze38Or1r6aaQrX2Z0usGfpeB0CukiquQFJ6z2qKvMJpQhxrZYcGv4OgO9IHKkWVR7e/jZxsQl95hNZLUa2qWCK5xinrngFms6wwCaoo5QoyRAXQmuuIIWnNJ7jxQLhMSw4DjBfbngdAK5ygtuECFZPxcFCsNsxh7gyNN3dMSVCSZGpO/sJjDMC054tEvnVIadLtAvFtwq03IDmEjBkUDW1RgensUOtWp46bmVCG6p4AqnWME3FUrIGqs6Gt8CHVmnlgmPiRJcSQUtOFtlPL3lZVhwnOC+XHDDYsHR0gMQvTavKMswrkcQCMGJF4mVCHPFwlLZXW9ecIPzx0uth1YIwTuC87AnhQ3ciZqLQsHRJl3bQEA0T909Qp1KBVc4hYcsWzrhvNwnSFGCm5NiDFSU4EoqKMENpKklS+CaGBYcJ7hv+B5cseDInW2FdBqksTcAvNp6vNeCs0mgNKT2meoefsgLTkhvQjmGAQD/tXVXf09wCVqkcIE3WbNYcM30+vs0HD1gJfaq5YIrnCIBwhOvpLC6CZAEt09NJbhMZ2+ijBBccYW84IbAMtM1BsSw4DjB/ZTgBE5zkyCp0hGjBm9mWkQ01YJT+lNbrhiJRUcmBVtUF4gpi+MjbLvi44f3BLdFnRQjYFkmODuCY/XT7sQeNcR1ueAKp9iiR0V0Ea0bBhFZWnD3pNiLyYXgiivkBecC3VNh3qKy4DjB/bDgBFX/9OeRNsFOC65DAuG8idANtBBniOyzDxl8LLRNTIeoi75NVCq4DRKDSC2CWSY4ekS7IYU4x8xBSOWCK5xig9Cicyr6bTNDC66vF75iRUpwokK54Cwfr5mm/T/3zmXBcYL7ccE1g5qlwkWohaV/7GrBrSyS9JBUpOBaqqKP2vnXRPbwXJIs8ET0iDVJTlvUyDq1l/8u3tUKAZUK7g2bLt6kj1dt7D8iuPwUuQsak4lsV+VWwbUWnF44AGItuOIKgnv1+9+fPqc2E+yJYcFxgvspwZnARLksOLnDs1SUUYLDWKe7tdQNounxDSugcy44M0HdkDEwitxUKT0SmDgKrgnscu0ZdSRDWXOD6KFccFV4flpX7FG32H1EcPkpxAX7rrzgHH7l7DkJmp8EF8qFV49IqlpwxRUELaHQA1X9jIMdwnfSI6bJT6Wy4DjB/cQW9RFe0yKqLD20Ml/RaJkWWTf1BKjK00PMTcOqxhF8W+gm9cvYsYzrHvBqnQuOxsDi2SCr7WEt89qdS2S0/ei4wJQPFli6PfH0wy+HjJu5aLJUcLQCaiRYA57xIcEt/jaFvYU/uSJr0NLbV2nMWsMgMm8jqK/XLeAvbarsVsCMtOCKKwjugJklpht6qB/OtZd1eAN+VIsFxwnuBwVnh4BfDyLI5yS1MeCvPCRLoCFPn66AxAPQHyjdDD3ASwDUbCoQnBUDSIIEaBnpdQMAYRghvFNb01sg2W7XmfbcMF2UQFqkXHCxkiA9A3P6kODc/BTiqVNEq/TIHZ1oAvACH5gFGMs68R0APwLQspTgiipojBDwVv3Uj7sEiLYRkOyIBceC4wT3g4KjyszHAa9rk8Z4S49F9wPLQ+d4ut310mV7V+tGJhz0Xww6E5zg5jWtUm+TwG6lq5O1PQAceeluAmCebc/dezhQW9I/Cq6ByNaJq/kxwRnZKQROS1ywN6QsDyscCJrUw/woOHqu40BddKYFV1xB4GyAYwAcbiIA0WZILDgWHCe4H8ZyGw3HoByGMx3aOT+mx9QyrZsrs+Fa9D72YKjOEKt3uTefRMlB/ggZ1enApu9DTJG/oOiq4HdyPk2us/IKYt6paZGgYu74vxlkwXGC+3+SCYBZwTEMEQuOiBPc7w0LjnkXFhwnuN8dFhzzLiw4TnC/Oyw45l1YcJzgfndYcMy7sOA4wf3u2KNRhfKYoxtiGCIWHCc4hmFYcJzgGObPhgXHCY5hLhYWHCc4hrlYWHB/sXfHrYkjYRzHn0iYX0yNISqjsUorikHRioIVBREt1v5R6Pt/N3edccakpluv3YM79/n+sXdkNU5m8cMTt9vyBMdxVxsDxxMcx11tDBxPcBx3tTFwPMFx3NXGwPEEx3FXGwPHExzHXW0MHE9wHHe1MXA8wXHc1cbA8QTHcVcbA8cTHMddbQwcT3A5Cdct0ql/dXcc1w3o73z1n2z5xwuu6/x68a5PmYruhwsat7uroSCT5x7zBZ3n7dtvw99zoT/4A/H0ZrgOcQwcT3A/ygEmdKqHmP61hkDL/Ei+s3KP3wIufV4RQOxRui2ARzI1yhLvJXXzqBVMYfkwpmydCMDmN13o97I/VXAJBMQxcDzB/dnAoZ05EqeAc+oSkEklBpDMDXDp6oJSzQG5fGrStwv+FeBEkTgGjie4/zxwpeWy+7uBS1CmVPdYSwNcUAbKU4dI+D2JuGGAGzjvee60DCwEnVoiDn7i9yhOXehPgXtaLjVsveiFOAaOJ7j/PHCq3wxcHSjRqRpeLHDL1M2qmyAqKuDSZ2wBYzqVYEs/aPLjvbPApZNg4Bg4nuD+UOCGEepkcyEDA9wUeCPbXOJwBlwhwl2WEgbufxsDxxPcFQI36CERqeWP6AhcIUFZ0KkWYs8AZ3tFhYG7khg4nuAuB050XhNZHa0EHRtu1mFYObiUSTxv12FUPhTVc/sHMt33N0qgejmJd8spqZx+/zkDmXP/Wo2T2YtzAq7QLUfxulX6CJzz0K/GUe2l+BG4G2Bvl5OgaYDrAo0PVj6fAbdAlXSlfr8P4O9fB0SP/brdkL7ipdnvEQ0XuzgZPZDJe6lF0fJJne/JPL3/pi/UbtAujmpPgT1dk8R0mcS7O5coZxcscM3+Ir2qflDYqqXoWv034hg4nuC+B1yhBl3N0/dyC+jkM6XyytCFe0WKtcOJ0COiTgxdX5j3bhq4mwS6atEAV6pCJe+zwPkV6BL/A3BUweKEWFgwwG30ZGdztv3mGXAVzAzgMN0SLTH6MFXWUXZa0N2Jo4kRVPGKiJYwLVJTmGMOx7fmdPViGSrZpZxdsM+tI0qvCiVaIPRId/OuNcfA8QT3PeA2CF+GxfFBoq8eVAZGq5LbrCFukE3MEC/aJbcdoeoQeSF6pBtD+kS3EpX6PmjcAe0c4IIEyWHqD+rxkagylglaK/e5HgKdNHB+BNl69ofdSDGQAa6L2LMDWYsMcDVs6LwscANpV1zsdDrA7u9fg0+A22Dde75ZVYAumeX39v6+rw7sO50q0Pm7xulCxRZojf1hu4qwcTxdb4fXSeP9SuTgbBeywKVX1fFocPpQ8YDqn/s+ZuB4gvshcCLSItEB8NWbDRM9g90hLJGpYeaIOTAlohYih1R9LNUnXGXHfNSVA9wjIp/0/6CojyMcqyNuFWHxBJwoI7zVqqxRcbLAFSXapPJiNAxwIsTTV8C5a8jS+add+cABI0ddRBVV9dprRAHp3wud9Gdw9kLFwlyP10c4OF7icV2uxOZ8F7LAZVdFM8NaIeTP5Rg4nuC+DZwHNPUbc7MZKjhGhhQ9penu16+kS9RJBsCDfpR8l8+prMekaiMW58Bt1nVSlYCGPm5RGgMvJ+BuT4t8BsZZ4GiLsnmZqjDA+UD7E+Dqzfc6T1up2LwQOIM1vQAeET3ZYVZU0cwFbg48ks6LMNOns/u3ROVsF34N3IO59g5i/uJfBo4nuO8CRxFqHtk6yhFdCwmdVzb/RKGvDVDSmBRQwRlwmTU09fHQvmoFtRNwCzUa6nbYfADuASgdV/FEBrgA6OYDlyq5ocuB65yYcZVqM3t5j9Nc4DapZb9A+hq4kr3NjHJ2IR84K+nouKgFcQwcT3DfBe4NiHoNx6IG19SCdChTsO+2oNVpQgYKodQ5HbdZDwH/E+BEaTy5Azr6eDn9VR0n4NaIXJOFxQLnRKgfRyDfAkch6p8Bt3uv8rpoenQ5cBomu6Yi0KNTucCtMUrfzk81cKQygmV34ZfA2b/GcYEhcQwcT3BfJwwEmQFN9CSAcHEr9CdqmQKyee27CCoFnBMp2Rr2DmpYr0mocoHzX0YxVJ2Pg8kE8CxwIdLtPgBHByRC3TTOyABnT5b/GZztcuBikQFuADS/Ai7EIb3Urjrd8gw4swtfA1fQZ+yhQhwDxxPcJVWMNqoRXkk1OCi5yoF6v6Oaqpj57huy2u+1j8BRDztB1DraUtwCCMubySEXONGLgbhy99S0wLXI9AYULXBxZgGvWeAUNnt1A9dJAddC6FAqZ1ed/AS4iDLADYHpV8DFqesJgDdzOgtcdhe+AE4fDD1yIrSJY+B4grukLWp0qoqW3S63OwN2jrJCUE5jYDZWt3mzI3C+xJwKIRrHLy4JH11BRPNc4HqQG3UbLCxwIzIdEAsL3A59Os8Cp78Ubo7YSwHXBMaUag88/HPgBD4BLgDqXwG3Qy29V6sz4LK7cAFwgUSXmggLxDFwPMFdUh2xTyZX4u0DYfdEXcDPH/6WgsgCp2nYUAcV8+SGwSUHOA+YGA8McImgY69YkwVui6r4FXBvCD3aYEEp4ERN4WxrIfQuB85MiTefASciLO0yXD8XuC1iu4InwD0DLrsLFwBHC+zEDAfiGDie4C6qJLFJjXNhQES9ysEatiEqytNct5/e0DFHomPmHHOOZ4Te7HgH9Ygq6Xp5wM0tmzcWODRJNwDqJ+Cmp99wptPgDLiiRKcQ4jYNHA0lWiJNdY8uBW5jVz75DDg66K3SHj7px0pxAi677MIaFcoDLrsL+cBNyDYA3oAScQwcT3CXdYC8J5V4g8bh3n5jtBoO+iFzUrWBod3P0Ix7HQucqKJn7qDezJ2thzzgBsDAjCUWuGqgPZghLp0wcWpIAn3+BSLvDDjqo9xEIjLAUQu4c0j3HCIpXgxcB1I/aCo/Bc6NUXO0+VIGx5vi/Qk4vexY75bYQj7kAJfdhXzgdijTqRlwHC9Lrst3qgwcT3Bf5UVA/9l3Sg+vQNVRcERYN4goeARWx/fnpEhU6kosyDZCNPaIinV5OjwBzB1UA2i5gsRtLQZKZ8A5IcoNh8i9k0BbH18iWhXJ26+VtBYTKu4QTQskBi2lwBlwUyBBj7LAFVpA9HjjOaXxCAhduhg4H6gMSNxM4qifD5y+0uWzQ6IdHnV3gb5HJPSFmn/tcO+Tc7tQB/KAy+5CHnBb5aYQdhLFlN5LgDlxDBxPcF8UvAKABIBt8WhTDCSzKoCtUCPJCECSQM1ENjcEZCWRGB0wMubEJ0E2AKJ1iHgFNM6AoyaAsBIBjxVM9PF6F0AkAbREGhMKEkCuQwBdygHOiQC4KeB008heWc2ly4GjtgTCCIiGm0+BE3UAcSUGWg6p7oB4t9ucLpSCKoBqDOV1LnDZXcgDzpVAVIlKpBIAHAaOgeMJ7vJEtxYCCMtNMvkbxULSdUhVmCQAUFkJSnWzBIDo0XlDQscWmNEx5y0CIEcDEaJzDhw9rNU5m9TH4ggcPdcUR6sUJiq/FQJAf0h5wNEBqNEZcBQcEkXcrCPoQuB0q4oE4lZAnwCnun0FIGttOwv34tN3EzELUMsurygPuLNdyAOO5hXAfu5WeLeSgWPgeIL7Rwl/7gtK5/jzYSAyjxgW6WPeYF9y6NMc86T8RNBo+PSh4mBQzD1Xae8WvnFhw73r0T/Pm1/wasXB0Mleb2NQ+LjsubqeS3ch/2XsA+4h+YdtMXA8wXFXmdhhSxwDxxMcd43d8n0pA8cTHHetLbH+c9/ADBxPcNxVV5LoEsfA8QTHXWMHhB5xDBxPcNw1th83iGPgeILjuD8sBo4nOI672hg4nuA47mpj4HiC47irjYHjCY7jrjYGjic4jrvaGDie4DjuamPgeILjuKuNgeMJjuOutr/YrQMSAAAAAEH/X/cjdEQkcA4OtgTOwcGWwDk42BI4BwdbAufgYEvgHBxsCZyDgy2Bc3CwJXAODrYEzsHBlsA5ONgSOAcHWwLn4GBL4BwcbAmcg4MtgXNwsCVwDg62BM7BwZbAOTjYEjgHB1sC5+BgS+AcHGwJnIODLYFzcLAlcA4OtgTOwcGWwDk42BI4BwdbAufgYEvgHBxsCZyDgy2Bc3CwJXAODrYEzsHBlsA5ONgSOAcHWwLn4GBL4BwcbAmcg4MtgXNwsCVwDg62BM7BwZbAOTjYEjgHB1sC5+BgS+AcHGwJnIODLYFzcLAlcA4OYtcMUhyIYSCIRDNIRv7/d5d1Qg65jo2GUNVPMBQF8s+C4LYW3BU5SgBwixoZF4J7WMHFFABsYgaCe1DBRUmqmeEGADfwyFmSKhDcQwrOhlTTbeGMsRv7x2dJwxDcEwouJOVbbhQcwB0+lktJgeD6Cy6l4etdKDjG7u6jOR9SIrjugpuvfKPgAPYV3CKlieB6Cy6l/GQbBcfYnoJbSykRXGfBxfIbBQewv+BWwwWC6ys4e/UbBcfYrn2fGgzBtRXc0DCj4AB28W25oYHgugouJH+/CFdUxvYXnLkUCK6p4EppFBzAuYKzVCG4noILlZlTcIydKzgrBYJrKbipaRQcwMmCs6mJ4DoK7pKcgmPsbMG5dCG4hoILlVFwAGcLzkqB4BoKLjXXG/APjrGDBTeVCK6h4IaSggM4XXCpgeAaCq4UFBxjhwvOQoXgGgpOcgoO4GzBubmE4BoKTjJzrqiMnS04Q3BNBWcUHMDZgjNHcBQcY78yCo6C+2O3jk0QCoIoirImi/J/ESIIEwn2X5zBilawwTzOfQVMNhwpNYIjOLPcERzBSakRHMGZ5Y7gCE5KjeAIzix3BEdwUmoER3BmuSM4gpNSIziCM8sdwRGclBrBEZxZ7giO4KTUCI7gzHJHcAQnpUZwBGeWO4IjOCk1giM4s9wRHMFJqREcwZnljuAITkqN4AjOLHcE10twl6pz7O6oY/w6q65DahnBNRPcbc7HbtiN93z+b7zmvKOk9RzBNRPcenB7Ww/u23pw0oe9s+tNFIjCcA4heUHRCWD4Kk3XaCSaukaTLdGEbLCx9qJJ//+/WeEgWNfutjdVm/OcC5EZhrl6+9Bx9CoRgxODe8fg9m+i5fJGDE7qOksMTgzupMHJCq7wHRCDE4P7t8Fpspgrdb0lBicGJwYnfFvE4K7f4LSfIze0e36r7m++dhPlxBZtljnxSNawZ9vdB5MGy8f6lGOHbv5UXbXvMzPfGBxNlkuLdgyXfdJW90m4zsdvZ2AMXtwwWcyMamDT79m7Xr9IBFBKuwSFE4O7YoMz7sGEU2ICGyXeKoKikh8hSmw9xohKZh6YITG3VZ9E54CrmAJj2tGF3+lWA7/SARMbjNuigrECE9OOres+kyB8FDG4S+U8BqflwO+5HgxcqA0HTggvjsZzPwyHVcANAPU4nUQpkrQKry3g/gj0eQ7MON8ANVwFP3IkTm1wbwJuu8biYRO82vCCZg6WDTuOrMAPcVdO2UU2aFv9JVAk2x3gi8NJicFdPWcxOC2FmlOBuYQKijMO1BOrlOtxwFkKGQ+/Cj2MqtjKTSp4BvrFwArrNiedh9MGB/hU0PaQUs0jbKs6QKe4K6ATz8PdB5wgfBgxuAvlLAZ3AzwS07Gx4EB6qLOJA24I/CJmWIVXF7ZJTA8OEfnADTExThsctsQs4TRzSNdDKtH5LnOgRQVBmnaIJtOpLgYnJQZ39ZzF4FLYBlXM4FlEv6HqMz0OOBf3VGGGGHEYPVNFVCrXGov6Ht47BqcTs4VNf2OwCraBWJZghctADO6qDY4owwv327EBVkWodeszcRlwJuDzmfKCEYfaYFzRB57IAIb1Zet3DI5qDbTp6E+kPn/IgVvaMQKyWVu+DEXqAkoM7soNTiE+bHslSpDur6dnKNa1W9ozwoiKhjf0Sa+Cs+T+tMEteVAOuAP0h5cQBXybzj12JNsxCcJnEYO7WM5icCFi7sYB90xkI611bQbFD4239aklRmUDVNLws+jTrw1udNrg8pMGp21DIMxyv7/PUW2el4EXG+JwUmJw34WzGJyLHu2ZAxGRgy4xR4+oDD9+9oGADunw0gTjnDa4/KTBbeH9/mUUTQeiaGz8NZCSIHwWMbgL5SwGN0JoUIVfRtEdlNkklaIdCe7rIOMFhAmHUYOmmjgy1EcNbodZJ6PxdkxtC7RF4aQuQOHE4K7W4CKgT4yZwSGiVfXBET5ULHLY1L7FdpZhbRAziaZElCJsEfOKTxjcDWDxEYem1s1u91kqXyQnfBoxuEvlCw2uwegh/MVdR/BWfEZNqWCcVAGn28h0zsOwCq+ojsGJwgMH1R3f07LxCYML6ofdlA0uh2Nw4HpYEbXa7Y54nJQY3NXzVQaXBjVjok4Ge6CT8XQHDLiLCy9etX/6oUqhqGATFlu1xlEKp4vRXtPuLKJWlFQulwLdwKBOX3nd9w2OtCODMxS6G4NonHs8gScPoyKsxzm8luxkED6JGNyl8kUGd4hT5FkCwA3RPJm2FUpU4ENRSeRVF3TqjfQ+ALUGkLVYuO4BhAng9eP6Nxn+t4rK6xVQjgIeHZ7BDPDWCxvAq+xFlRKD+y58kcEdBxxZW4Udvajp5DvK7j12DlRr/DtTyaJvUK/Oqb6DHfbMJEZ7dbHjZUPxv/4Hp3HANawy7Mj6tETKvrhAQW9FshdV+CxicJfKlxgcncLQb4JO070hx4KOsA92NbSCjaXxdfxi8Thvbs1o9cvf7Vprs7HosKPZfppUE5IdDVIkn4P7Dnz5L9sfJxofmAcjZYjLINNbVNEBItLeDM5HR+NodOIdX3fcftTxrwnJlwMLH0YM7nI5xy/bMxoXHzTLmrQCItrx3OzIjxFaTaZxNQZXHxy1UnMDOtFetx6PzC9icFJicNfPhRgc9eBOqGBqY8napvDCT4zPHmb0b4PTxOCEb4MY3LczuD/s1jFKQ0EYhVFmmiEwxEJIDL5CCWhnEZD0Bnzuf0XywiOkyArunO82w7+A4ZT+3Np2ukzb1j57ufZ7aIePeX/+ae1UC8HZKCO4PMGVft61pd28KWvfp3bt6VgLwWmYCC5OcMuxv1+mv69+/3G9vO3n4+tmuRCcjTKCCxRcLY9wtkZwGiiCixRcvW093N4EZyON4MYRXCU4jRbBERzBWewIjuAITrERHMERnMWO4AiO4BQbwREcwVnsCI7gCE6xERzBEZzFjuAIjuAUG8ERHMFZ7AiO4AhOsREcwRGcxY7gCI7gFBvBERzBWewIjuAITrERHMERnMWO4AiO4BQbwREcwVnsCI7gCE6xERzBEZz9s3c2XGkjURg+NzCHhA/RbhEKaiVABSmK4idQoBY/AEH//6/ZubmTmTTNsXp2z9aw952zdZhMZpLUPPuEBLq2hQ2ODY4NjrO2YYNjg2OD47K2hQ2ODY4NjrO2YYNjg2OD47K2hQ2ODY4NjrO2YYNjg2OD47K2hQ2ODY4NjrO2YYNjg2OD47K2hQ2ODY4NjrO2YYNjg/uXDA7Y4Li8u8IGxwbHBsdZ27DBscG9aHDwSoMz+XMGB6yKXEKFDY4N7kWDux+Pn35vcK3Lv1Jny08f686fM7jKeDxOAofDBueHDe63BlcQYg9eNrjswUz46S1rf8rgNuT0++xwXNjg/LDB/d7gEHAvGpyz1SO0LbquV5mm4Y8YHAGOw2GD88MG948N7nwghJgc1BxsaX15lq8WGX8hGxyXf6Owwb2L/C8MLrS8Kpc3bmzQqU2EWOXY4DjvI2xwbHD/wOBKbSGat9hiO0DJrYSYAr8Hx+V9FDa4tTY4eLPBUaINLmx49kCIK/y58ZwQ3QMHLorFUqYtGsnXqBsbHOfXsMG92/x3BgfZ/kU5iYsjsKNfOZXjahbCV4v27XFH2RbWT5zQ9SmkyxcdR7cFDS4wL/13LUQ3B5BsCi/PLfnHD7gR4kAP6dwd77aMyoWhrDb7sFY7tCC8561aNQdesL6bDq6qxi7LxiiDA7tUezp3og4gLrmzg0sAkuWLkzSENwCy1acM1ajOfhi/wgYXO4NLnw4EZvDowanU7vXah+DFWcl6xWPXmDol8nTiQqfX6xUhuVWQje4ZnreH2wmsD0vg5avskIN7D1bu/CRgcFHzYpy2EBcAyQXOM5I9z+SaOci6/irW/Z7AtLdagMnLKfJAuZT1KWD2N13s1BjeAqWLvezrCbauyjjRxsKbuAYYtSvlpbdasxhhcLvzHi7rXZUhlNKnAi4pTM3hzvzVVfvl43TZ640AfniHojvGlp2Rtx/f+UMZMQsbXNwMDqoL4Wdw7p18eJpT95SsfsdKcqY7FfqAOZHVeqcrKIk7eCqoeq+qAZGeChV3HAJceF6cmC5Qr2TvDRtsb90RAkpMAJNsmo248IiIhHwAzLmE6wyBYi2FnvO7nnM7rde9hMOBXz81u/LZFSopKwQ4e9sM+fHnYzhuCJVFXx3gekLoNsXDoQSrlRcqU3D0Np6xxMWrsMHFzeAeXORFc7qHfGp7ZoRk+YiVoqzM1Tv9MrOrsy7iyPapcF3A1q4HopqL9YXXz/EBMcWxBwSB+wDgouddCnEE0JevHz2u4GAHstIUDc+McKLG6mroTeIR7lbCpJvGviO5qKM2XrYt5wNEbcmfMzVC3kxcZLFH5e4M642KvytTfDUgRqd+BpzlaeNMDunSBlGoD2bSbOPadRJXQptswrYHDbgtcyiKm7gZgx7hlhOnsMHFzOCSbTyjkUgOnuN7vhg1TgBwGcHqVC76lMRFc1n77FOhISb1LPju1h4nlZfdm5MfL1jt2gQXp4OAC89Ly7oAIGdY2OCz6gkARmLhc6aZAZnrhhwu6dvmEgAO/M06wk6eED4SnWnOhuhdlwBKK+VhFYAWjpeiXcHMdi2A802huGYA9xcCy7PSGqKxZo7iLhLv5lw2jOUcbRu9FJvmWXTKpsCtVIBzXZHvW5CbCy9XVRucTzgrK1y8ChtcvAwOIfIBKFd0+gJUetLTHNiUDtQBjGTBCrykG0EqLFrgs0S0qWsdLUcD7hOANsBvGnDR8+YkDgFgoNfakmBCBLbFpmLZptqDSwSL3v4x7Ls+zG4kS7LgZSR3ggBnXKrj8W0HMK2GZKHelVGODpLCrQFcyyU4Y25dXKgzMEaHAovD4o5uqOONMJsS4PzdB6drHNGS67s2cGIUNrh4GZyTkJRygFJqqBMSxsimU3MFVXt4qABlRqc4UeEOgLSJXAuTJaciQLT9oWsCEakBFzlvxfvTli++UPsZ9c0h8TzIuh2gWHIrJuDbZqKz8FUTjh4eqobdDcsH3FfAUP3A8Kmtd6UMlLTs4aYDgPuG1+JgxhQt/zCW8U6vBZQh0tJrWvlNWTlUwlGAOzP98EjotzgrrHBxKmxw8TK4ohEp0o+ZPpExV7+slnOpD1EBDNSEDZSGOpk30FpofdIpkdWAi5y3KkQe4FZj1VrQAF88N0ojTcAPXt0lQdkmhlTTAhNnSFMS1M4Nn4VPwGcNuOCzK3m6xibA0cb17ODx2qEq9bzWv+ZHRx2zMg5FF851BbXvAahtAeWDrHeAE6OwwcXL4NDSEnM/+AK0GJEV6Vj9r6m9rtdsqGAAN6HRfwZc3V8XcOwjDbjIeQ899ctpAFyqK+aVmNnKEoNriD5o2yQmaryVLvPDiSsCgHNpKwhwdgTgPuFiPe1pAHCF4Lx0BaoO55BgaempqelWv9zB3qq1EgDcjyDg2ODiVNjg4mVweRGOYloZ63fm77J/VhAqBnB/BQCXggiD6+hpb+SrYw24yHkt13tLrK3e8rprk3htECd/iFA0JpBkA9C/cJnUQqgYwDV96My8vmCFAfeoj1ANCWsA54hw8oAhK3UdAI040j3XVkPRDeFtApxLbQS4NBtcXMMGFy+DC4HG6M2ZIPug2FcC486GW0HA3QQAt02DBwFntMXybkU+aMBFzzsRvRwRYDKufSsgUWvONWEvDDg1HBBFCIkWPV8sMIvn7TYBTs/pA24FEQZ3rVYnwB28BDj6WIUGnMEbNYmcfvmEaqgBZwwuxwYX18IGFy+De8TrscNAWtR+SkCrBkRvcN2x6RSOBlyUwRX1tHMlKwibyHlplq/01jymsS8J5SaE2Mz59z+Hh8EQitPka8PAm2Ttm10Uq60Q4CwNuAiDy+sj9JluSQQvUQuHweQAzP8EqtrgdNOTHuqjf4kaMrgcG1xcwwYXL4NDL/oAJtTHe+wCH+pdpAFTwjujlnKUtxjcRz3kCs9rDZvIeaHkions058ImV4d6h5kU7a+u7EZ8euGz7JM6RoTI3E3SVN16y0GZ4bOE5g14EZ0kyE8r+p57ePNSeIR36KdtgwBi2xw61TY4OJlcE6BHqulpLNZB2SSXbzB8KQfbrgP3HoUbzG4rgPmYq0ZgE30vGf0pFtuJz89RTSVP6TqaVCRJHPvQCWXzRIlvuENBqspha9MW2KoOnqDwSFoqDmdkGM5GnD087s+XtksDmnep9yzgDL3Bj4S8ocDlBbKn8MGt05hg4uXwcF24K22r+qNLRt50aFnMb76rCrrG4NvMDhxEHjQ99HAJnpeyE6kKWajf6k8nxta1FLtqaEf6Anfw4Lw5A9ODOBuxVsMTuwpLE0J6wZwSZe+4wSTnXmczlzKOD896HvSkKBVVF2qncbFKWCDW6fCBhcvg4NsF9+AsnHxGE9z/9rui/+RrT5iBM9aB9H3pfEWg8PVkqg6M1mbOBo2UfMSlOTiNqJDJXmdBwgonHhOenO3pRql0ZHaCmxjxRXHlQ0ZkDleCJnkaw1ONqNLZYaC4G4ABx9x48kPR/TkypMaetdFnrYAoNhWTzX3G0g13LbSMypsFtjg1ilscPEyOAv28Yxsb25vJvB8rABAXV+aHjWIHznvw+TN1LAr3D3Z69UGt4ljjgpCxq1BEHAR82LuRjjTcGP8VK2f5psSIHf6lyqLyOo1U8suDlf3P2LfB8xSQRlnFIPpmQQZAub8dQZHnQujrsB8CH3YfojzrebTGT0kYgCH7MPpNhe41TtaR0VvNFy52FYDNri1KmxwMTM4gP5C+FkgD84TdHPBl5clXQlS3Gv8gKj9WoOrzYVK4hg04KLnVQTe6Ilg2vWAbe7p5kbRh8UpeEl36QsCMm2hMi/iBkQbnAVWCHA33wWG+Bb+uqR88BmRIODgsiFUulWgBL8uqQ/ABrdWYYOLm8FZkN6Y0On46NB1qXk8xGqqd9jLxJbmMSAI7l5rcPv2Z7olmipBGHCheTXinPulj4j2/MI2Gy0rO02iZT7jvx84BJUHQV8I15p6MJ5cwzm+hfhag7uBJ29sd7gf8YWX+8uGt3DZh58BB5WpB+TePKN/5Q+3CLKzjTQAG9x6FTa42BkcprV/v58JdQ51z1bvay3Qie6m6wYQVqt2XHH0/GYtPW/Ev/OQPDq+3y/ZekiTbLn+ULJf3IbcSf24ohtCc4brBnA49o+TXHixqjqdYtF88zpFL6mXvSW6zT5/ut9tRc9q6vxtvjEMG1z8DM6caMF+5oduDLeYRrOyqSvAhVcMt5jhzPqhTi9uqhXehuCq0XOG1yDAhfuY0cODRm9t8F8Ze83M9JP9LV6FDS6OBvfr355uCJPR0MgU00vXtcGFV6RXoXpgVFMN88K0hTuYbYgaP7LNrGEMzrQHF1NVl+Ci8JIwkbH2Yp01LnZhg2OD+8cGR1U2OC7vr7DBscH9SwZnscFx3l3Y4Njg2ODY4Na2sMGxwbHBscGtbdjg2OBUPbO7u5uLhcE5cktbbHBc2OBeDhucqavEwuC8sMFx2OB+Eza4X60kBganChscFza4l8IGxwb3N7t2tNo4DIRhVDZDkIz8/q+70a0ppstayDucbyBQWkIo5OcQQnC5IziCIziCS3sER3AER3BpIziCIziCS3sER3AER3BpIziCIziCS3sER3AER3BpIziCIziCS3sER3AER3BpIziCIziCS3sER3AER3BpIziCIziCS3sER3AER3BpIziCIziCS3sER3AER3BpIziCIziCS3sER3AER3BpIziCIziCS3sER3AER3BpIziCIziCS3sER3AER3BpI7j3CG6/6IDgCM49LrjdwC0RXI9KcASnbaLgxkONbuAWCO6IRnAE52YLrsVh4BYIrsVJcASnbbLgzmgGboHganSCIzg3W3A9qoFbILhPxE5wBKeJghuPER8Dt0Bw5Yxz8z04gnNTBXfGWQzcAsGVGp3gCE5zBdejGrglgis92uYzOIJzEwXXohcDt0RwpUbsBEdwmie4PaIauEWCK0ccm8/gCM5NE9wRRzFwiwRXtohGcASnWYJrEZuBWya4UsfCERzBuSmCaxG1GLhFghu1iEZwBKcJghv71oqBWya40TkWjuAIzj0uuBZxFgO3QHAXwx07wRGcnhXcfgy/GbilghvVGIjzPTiCcw8KrkVELQZuueBK2Y6Ifu4ER3B6BnD72SOOrRi4FwjuW+0xNm78P28Bd/nxVnCXLn91ee4bwd2b6V5wox9e728Ed/dKf3iOX/3q7wW3Edz/ddt4Q451i/7lm4F7heBG9QxJD3XWUgzcawQ3+tR29JD0T/Wj1e8mGbhXCU7SuzJwn2LgpKQZOIKT0mbgCE5Km4EjOCltBo7gpLQZOIKT0mbgCO4Pu3VAAgAAACDo/+t+hI6IYEvgHBxsCZyDgy2Bc3CwJXAODrYEzsHBlsA5ONgSOAcHWwLn4GBL4BwcbAmcg4MtgXNwsCVwDg62BM7BwZbAOTjYEjgHB1sC5+BgS+AcHGwJnIODLYFzcLAlcA4OtgTOwcGWwDk42BI4BwdbAufgIHbrgAQAAABA0P/X/QgdEW0JnIODLYFzcLAlcA4OtgTOwcGWwDk42BI4BwdbAufgYEvgHBxsCZyDgy2Bc3CwJXAODrYEzsHBlsDFfh31pgnFUQA/KCcToxVUqtHWZSqTlnV1wy0uNlSndVGs9ft/ml2UVB5NxMTU/+/J6JF7n04OsuCE+LCk4I5dcPfzWFPXcKzOZHJzYEoIIQV38gW34V5wpeEor2T/wJQQQgru5Atuw6SNIQUnxNmQgkthwQWVSG85IjnSpeCEOBdScCksuBJiXYcc4gj1RuP7gSkhhBTcyRdcsuBQJZ0chBDnQQouzQWHOskmhBDnQQou1QWXIdmBUrgKvLYXfCtiyzLNBjotz3kBTNPMYb4ct8OnBgBjFdj+2jIQuTHNCiKZr25f/b+Xx86jOXayo+FLMqVo/6LvF7MGEucUy2v1xOsidvKWukroTjIQ4tJIwaW64JokfwF49rkT6oi45LRK5QEgadS4s8I8TAYrpAlFD7njT6FoJmO9ZArGmrGB8X7Orc0t7wcib+9XuQdQcxynCiEuhBRcqguuRGYzQJlkf2ANPHJciIunxH3BffHpux5J5zFLhm6bpJmsroAcz/7MxqT/AMAi7ddVaU3ycyJlBFS5QcsmuTDic8oOudj0SY4yAHSbDKzV9ioq0qVKQIgLIQWX4oLTfpK8Bm7b5DAHoPhEjqIPLpXB252hASRtv5aBNnWotOpAYUZS31fXnYoUo7u55CcAYfzi2yMXcSruN+83AO1vm1wC8TlWAdBUhtFvz6QLJW+TXSk4cWGk4P6zb7+9SUNRAMYPyCNUBw63CSoif5yCiJK1yCYMa4Q5QZjf/9OY21tajDVG0nc9v1fLcrKONHly4NIUNjiKxuJ4BPhlkSb0JOAMoGHDE3UFoCXGAuiZ/knpHG7jdH2EphhLz3skUgLXjq08z4mmKtC5kUAFGIfXeWNflg+ndqe8FuOV501E7nzffy1KZYQGLt0nGbZ1kYdAW6wT8MLw5MQC/DBL8aAPn+PALYFJTiIDKJbFiqd8KIqV86EaXie8lZtgmZTXMGqJUtmkgUvxWVT3Z1ClGlALbWBqwzOXELZFNj7kJTBlP3D358Doaa0sVhVwV5P+b4FzgK8SWkDTXmcb/8YE7ugM2J509QxVZZEGLoUNzntr9B2xrmDfwIanKiHgRRS4rSQFTurfMTrHNTHyMwLbH/k4cPbENnQBvr3Oye+Bkw9nGO6lPvygskcDl+YpqnWRGLiKhIBPUeDmyYGT0uPvBC5zYjR6BOaFaGq4H7hKFLjKfuCMwpMBRuedKJUxGri0TlFj34BC7OiAwBnLL6vB3tnEUaPoA81oqgw0JORBLyFwVq59OjsHXohS2aKBS3+DWwJ9iR0SOCt3Cvck1j2H99HUCJ5KaA3FhMDFHA9molS2aODS3+BkCwuxahcXN/8fuO3aL9vCDaAgxfX6NlrUGtFUFc7GEvgCPEsK3Hi9Dov5HHxRKls0cOlvcNKATmP3k/vg/wO3gaoYpXt0SiZfvbwYTehGU30XfPPX5a4DPUnc4EZg49gORrrT6fSlKJURGrh0NzhrBXgvW69XHagc8Ba11YHjynB4NQ+q9GAUfNOj3tiA60RT0gDc2dXJHDh7mBy4x+CuJvXW4xG80ScZVMZo4NLd4Kz8gp3rgz6Dm7AzeCsiw3vs1KIpM3ZOyB9KcuDkkp1eXgOnMkYDl/YGZ31tYhy3DjxkGG46AG6xL8bRI5u4WVuiKWO5cAHW1478LXD3a3OM0akjGjiVMRq4eINLV3l4e+PI4XL1buttLv43C+27cUn+kB/ftR/+4+45z2+fFbJ7h3+xd8c0AAAACMP8u8bHaEUsfHBM4DzbQ5bAebaHLIGz4CBL4Cw4yBI4Cw6yBM6CgyyBs+AgS+AsOMgSOAsOsgTOgoMsgbPgIEvgLDjGbh2cMAwEQRAUwhidUP7xmgM/HMCBRauKjWAfQ5Nl4BQcZBk4BQdZBk7BQZaBU3CQZeAUHGQZOAUHWQZOwUGWgVNwkGXgFBxkGTgFB1kGTsFBloFTcJBl4BQcZBk4BQdZBk7BQZaBU3CQZeAUHGQZOAUHWQZOwUGWgVNwkGXgFBxkGbhVBbeP85rOsW/ALRi4JQX3Htev8dx3wp0YuBUFd1zT63vTsQF/92HvjlvaBsI4jj+px/2SmDY0LVdTM2ppMSi6sqEWBSl1qx0o9P2/mzXLXS7G6iyZMMjzYQztRP8YfPkluW4cuH+w4Dydt4z50CPG2P44cP/bgmvruon8l/6wTbtJITyy9vvBgRBCUpkjhPDJaq3Gm+F1q/TjtMAhxpqGA2cXXJ39Vl1wb284B5iRNUVMH3cP4JjKJgCebWtHMTLhPKCcB0NFi5Pm/jWzZuLA1V1wbhBUF5z+xP2cwM2prF8O3F0IoBuFAOKJDZx1y094WaNw4GouOGnzVhD6E/kJgUsRu2QJqHsTOGcB9CbZn3onXWBjAjdxMq1gNVKI+N4gaxIOXM0F59mL0uTq6eDpKrHXqd4nBG6g8IWsKW4vTOB+AadmobnPUMc6cCdkDIEpMdYcHLiaC85ut58HuZ92z31C4DZLdKggU9yZwLVDLKUNb4pI2sBpt+gSY83Bgau34FpBxvTNFE4EudYnBO4SsOF8ROiYwC3R9ci6A45fBe4G4BN6rEE4cHbB1ToClxxYibkP5308cO5Npxvfj87JOF/ch2G0FtXAOV0MyBghIR24Q+CGStwY01eB+wL4xFhjcODqLTjfXI1eHVhXgeZ/OHCii1yil+EcOfVYCRxNkUobsSMTuDEQUNn0dPAqcFMoPg7HGoQDV2/BFQ8Ung6sp+Iu3EcDJx8QfRHt4al++Ol0gIu7QAz7iI8qgTsEVsUg60kTuCl6VFUNnNtDnxhrDg5cvQVXPGI4KMtf3SNwQs8vGeWZGgAzSVvOCGHwMnAUYU65Dm7IBO4W3/8WOG8JjImx5uDA1V9w4nXgMmKPwF0CbX3nbeESuTEuTJRCTCuBm5ijcAGUXwQuxfyNwHWGf/xKQmBGjDUIB67mgjOql6j7LbgASCQVxsAZaQnSSuA8cxRugO9UBO4ByzcCZ6khMdYkHLh6C87XW636kEFkL+/xkOEUiDbCRg3CSKCcl4EjfRROphjrwJkXdwfuIXPfWW74CSprGA5cvQXn5S2rHBN5799MkiEGpNmB5t1iK10L0rkra1cC9zW/Y7dC6NrADZDKt+7BMdZQHDhJ9Q/6ispBX6NFO0QYkWbzRPJyGWMrcYjoFuiVeJXA6aNwC8xL3+EOOKeyee+UA8cajgNXb8FRkKu8VUvk0aNdluiT1UNCmnP04wFYEFGCUFKVDRytkUpqhViVAucrTKmkFWPNgWMNx4GzC67ONaoov9ne8GiXAWKfDKGwIUtOAUE0Afz3AncGrGiMVJY34BqxIGsIHHPgWMNx4GouOKkvUS074CTtEigsSnMubBPJTjTWvVQYZr/bXbf6dlgNXH4U7hkDKgfOTdF3yfC76PA9ONZ0HLiaC45c2zTzkebSbmso3Ry50W8gHaHvUMZV+JZ/yXXx7tHz14HbIDxUEDZwerNFPuVEhPiIA8eajgNXZ8HZi1RD2Np5byaxC5w++k7w9RnoObS1Ulj6RFIsodpEJJdQM48omCjM6XXgPIUUfSoCl5vEiJMjT7ZXawUM+SkqazwOXI0Fp7WLponSgmvTm9rP2FLYWuoMbgD18L0LYEIZ5wJAmgIYOdXAmYMkJzZwmoiKb9y95GMijHHg6iw4u+EMYffbO+SkHwIIO0Myrp+R6XylXGuWYiu6k7QrcN+A2LOBM5xZhMz9zONzcIxx4GosOMs1WSu49BfSv/YllbXE6tB7+RXnHu3NOzs+4/944Td7d4wCIBAEQVAMhBP//14xOoxNjrbqCRs0ky0I3NcFNx3j/fX5v+eElQjcXHDf7OO8Hufwmg8WIXBzwQExAndsAgdRAmfBQZbAWXCQJXAWHGQJnAUHWQJnwUGWwFlwkCVwFhxkCZwFB1kCZ8FBlsBZcJAlcBYcZAmcBQdZAmfBQZbAWXCQJXAWHGQJnAUHWQJnwUGWwFlwkCVwFhxkCZwFBzd7dpCaMBBAYXiSDMGERKTQfcGlGzeu2h7A+1+o1AuoUMj0+X1HmJA/j0wsgbPgIJbAWXAQS+AsOIglcBYcxBI4Cw5iCZwFB7EEzoKDWAJnwUEsgbPgIJbAWXAQS+AsOIglcBYcxBI4Cw5iCZwFB7EEzoKDWAJnwUEsgbPgIJbAWXAQS+AsOIglcBYcxBI4Cw5iCZwFB7EEzoKDWAJnwUEsgbPgIJbAWXAQS+AsOIglcBYcxBI4Cw5iCZwFB7EEzoKDWAJnwUEsgbPgIJbAWXAQS+AsOIglcBYcxBI4Cw5iCZwFB7EEzoKDWAJnwUEsgfu7BddP81JpwzJPfXnax/fX52mgBafPr+8PgWtlwY2TuLVmmcbyhPntOtCW69sscC0suOn2Pu261z3Htozd7vbFmcrD9qZbi057gdt8wXVzrXNfaEv/+1i68pDLYaBNh4vAbbvg+lqXXaE9u6XWvjzgeB5o1fkocFsuuL7W9XXPr23j+lDhju8D7Xo/Ctx2C66rdS20aq21K3dc7Le2nS8Ct9mCm/WtaWudyx3+v7XuIHBbLbipLq97eP/BuNy7S93/sHcHKw0DURiFZ7w3aRJikaxddOFCDIq4KrSN4qKgSPH9n0bpAwxtKMzc2/M9QkNPf5JpKyjdksDlWXC1Ks8Xytao1iGh43xI+caOwGVZcK12AWXr0hNuEJRvIHBZFlyvnH8r3Y32IYHvL1jwReAyLLjjewelS34KrQQWrAhchgXXahtQuuRV2gks2BG4DAuu4xGDAU3qRulWYMGWwGVYcL3GgNLF1I2EjcCCDYHLsOBUr/eVs6NOXV0OidgwErgMC44fAjYhdZkENhC4mQuOwLlH4BwgcCw4EDi3CBwLDgTOLQLHggOBc4vAseBA4NwicCw4EDi3CBwLDgTOLQLHggOBc4vAseBA4NwicCw4EDi3CBwLDgTOLQLHggOBc4vAseBA4NwicCy4mZ7v334eXsJlPe33xfwfj8XATevvg5xonKaDnGO9WPyKMQSOBTdHHF6ro4/PJlzQY1UtQyEMBm6K/06t1l2Mt3IOjfFdjCFwf+zdb1MSURTH8fvjcGNREApWSAETJDfI2hQRgVYcQQQEff+vpsPd5Z8hkvRgs/uZqbuul21snO+cdWPSE5ywEmJRISFWO3fkVOtQB84vTsF2aDWrQUwHTgfuP5ngElImnp6wxCoXZxw252cmc2zxwdmeDpw/mEGwbZNW2L1FhZgOnA7cfzLBFeRi4RLq4xVO8lK2vKrdtaQ0IzpwvlABrrNAhVZI49WBcyzrn/u/KHTg9AS3WDT1kbXyi3ekHG0JT9qUMqQD5wtHQC4EHNEKTwL31unA6QnOK9x6fWPXUhbPxVRXynxEB84HBgbSZBswbHqODpwO3P83wXmFW6tvrCxlTMwESMquYDjItYrmqF0SSiYePxC4ssr51rAjPMaFZRdH7QsIT2THKefLzteoDtzGYsAHohTwkVyJarVNrstqNU5UrVbBeDmdBC5+lDZKdxWaaCTrEaNU2LVJcarVr2Qn98NXRDvV6pCIMtWZBo3FM/vh8P5VjvxHB05PcNPCrde3CG/5Jubs9npJXr7Z0lW8nFwyFhxJJX8glK2edFkRoVydSdcgqAO3qTowIhoCdXKlgCS5fgA1Ikxl3cCZV3BdkKsWgCviNo831QdpqPveAvCeiLYxYxHR4AGeBPmODpye4GaFe7lv7EFKW/zuS5k75sTaA172vSuGWrw3Po7aWVqwaIMPyxWryKfPBfsg+ajyvsKvbUV04DbjAHu8mFuAQ2xJ4DqdDhgvXTdwGf51d2gA6BNTfYtmuycGEGgTuYErYCFw2Y4LgNHgvpV4b/byMgsgRn6jA6cnOMVt24t9Y6dSOuJ3MU5VmNcAR63vXpA9jjv2Pe/e1IYdzludv2u2R+6eLH+iZozL15SyYejAbeTeC8wBcE9sSeBo8WdwLJ0ziRp88pBY3wAyNh+MvgHh0WRTcNexy17gptoAjnn9DgTjxIZRoEY+owOnJ7hZ4V7uG2tL2RS/i7daN5PrjLxV5ozJS+K8JKUs7omxOh9tCZGb/nnhspQZHbhNmEEYA2KPQNAktkbgSj0aq7nPG8wI0CWlvA1kvE3b6rJPAueEgRtecwAeSTkG9slndOD0BDdhSSZeVFO1et6elDQJ3K1QPkvZ4KUn5a5w7QyHBbHNOw5nea3owG2iAnwnpQQMia0RuBgpIwA2UR8I98jV5mPb3dQmZSFwdgdI26Tmxe/kKocBh/xFB05PcAsTXEK8JKYmtOWi2euPtpTFyfW875CMClyYT1yJOSk+kfIMeYsO3CZSbsJYEkgRWyNwDiktN3D3wB55BgBy7qYGKQuB6wKGRawOZCseAEPyFx04PcHN+matUzgexwgLfxlMsL1QTyrTwFliPnD7aqSbcykXlHXgNjAAUNpXAHWzukbgDJPYNHBdIEMTW0DfDZy7aSFwMUz+MUoQC3bJX3Tg9AQ36xv//nLh0rznu5hTkbIthDGULN9qNmeBiy8E7ht/Pi3mnOrA/T0xLOASLQTuZGngoqS4gVP7uzQRBWrzm+YDZxnTnVs6cG/Qm5vg3L6JtQrXkLIiZgJn6vlAX0ozdAge1J4L3BZf+0jM6fKJ4ExEB24D3wCkPQBOiOYDZ2KdwF0C5+QZAXh8JnB2GujYpNwCO62ZMvmLDpye4GZ9W69wn3hLdeGdW2db4pxPZsXYj+cCJ8pSHgvXSbfbER1+zRf9Vq2/wlGPTj2tAGCRCtwOKbm1AhcCArwobcAYPBO4GyDskKsLXJB/6cDpCW7at3ULV5Oy/EN46kXOlmpYTyjvnw1cTEo7Isai3Dq+wkjd3Cqp09NbHbjX+wrc09Qd8JmXa+CIlKtp4E6AELFlgbPD7uuYfQtUaXngjgG0yVMBjB4pg1gsRD6jA6cnuEnf1i7clslD26UhGE75uBVWT0TzahpLy2cDV+KsWfASabnn85nJjrMtHbhXMyOARVNtIGIS1QBjROwe08ClgAdiywLHmfQaZt4BgTgtDdyjMT+0mbdAYUCsvAckyWd04PQEN+nb+oWrt9RbrmLvm/b4oDT+mvIcsZ93mVBxfOrdksCxH8S7axc7DoetKlif91YOPn3u5zls+hb19YbAPs2Uw0Cfu2UA0fuPB2kEP00CdwwELtq19tLAlU8A3J62M0EAp0TLAmdvA7i+dz0SjcLAdqLSTJ4AJZt8RgdOT3BcImvJiVWMkJzKfRFjP6WreFOUMrIscOzwTLrMBzEWaMuJn/pncBtIAQmak3FvMPsGlKCVmgSunMZYdmngaFCAJ5A0iZYFznn6sDa3Dc95j/xGB05PcIWE9TR5VkG84K6pWpVvHgnXu2tbMutQtKQsLA0c+zHM8yZ7WBKem5wci3/SDxk2MDAQWIhLBTBavA7rBhA+6JEKnNLrrggcmaE6mJGKE1srcDRIBsGCCd/NbzpweoJ7NaNTKJwbYgalwuHLX1n49mFxU/Tk7jYsfOgfCtwKdtwp06Ky08ytaNHAavJL/ojZe3xskR/pwOkJTnvLgfvP6cDpCU7TgXuzdOD0BKf9Yu+OcRSGoSiKvsRfUWw5CCFNj0RJQ0MFLID9b2hE2hkIVP753LOERFyeiFEIXFgEjgUHAhcWgWPBgcCFReBYcCBwYRE4FhwIXFgEjgUHAhcWgWPBgcCFReBYcCBwYRE4FhwIXFgEjgUHAhcWgWPBgcCFReBYcCBwYRE4FhwIXFgEjgUHAhcWgWuy4L73yq3H8Oruenv9J/53JHANFly1TvCus6qnLglrcCFwDRZcsVHwbrSip64Ja3AlcA0WXDaX7yDA+3fplrAGNwLXYMH1VgXvqvV6ap+wBnsC12DBzZ8d+LbwLeTvDaD46y4C12DBKVsRfCuW9cIuwb8dgWuy4AbjMYNz48JZnsJBEf+OhcA1WXDKVr/34q3BUJceBG0SvNuIwDVZcFKxSfBrsqIF2wTftiJwjRacOqNwjk22fBb7fErw7HQmcM0WnHqz6Xuvn2/DZNZr0eEnwa+fgwhcswU3F67ypMGjsc59W3Zgw/l1OojAtVpws66YFc7DedM/bkunt5z5Hc6r7VkEruGCm2Uzq3nsvvc6+jJ0Y65mlvW2DadFPDpuJALXdMHNhlwNvtQ86ANlx38avLnvigicgwX30OdC5LyoJff62P52vTDkfDherre9JALnYsEB8IfADSJwQFAEjgUHhEXgWHBAWASOBQeEReBYcEBYBI4FB4RF4FhwQFgEjgUHhEXgWHBAWASOBQeEReBYcEBYBI4FB4RF4FhwQFgEjgUHhEXgWHBAWASOBQeEReBYcEBYBI4F98u+veU4DkJRFDURQsHA/KfbIXai6keq+pfrtZiBP7aOQwxhCZwFB2EJnAUHYQmcBQdhCZwFB2EJnAUHYQmcBQdhCZwFB2EJnAUHYQmcBQdhCZwFB2EJnAUHYQmcBQdhCZwFB2EJnAUHYQmcBQdhCdx7wV33EUBQReDeCy5tQChJ4OaCSzNw9w0I5T4Dl64duO0ZuJ7rBoRSc7964LZjwe1534BQ9rzPwF25b2fghh/hIJiU8xC4eY1aR/aOCrHUGbhr3zG8r1F77hsQSM/96peor2tUEw6CmQPu8ncMx49wtzp67pd+DBBL6bmPerv4T3Dvbxn2nMcGBDFy3r2hvv8JN7qXVAij5ty9of424XzOAEHcswH3dcLd6lA4COLZt1FvBtyXi9SevaVCADV7Qf1zwp2FG54HLK2Ms28G3KGUL4XrRhwsrHZ9+1y4NhPnu1RYUpp5a/r2qXB7b+24f0keDSykpOO/EK31/eybwJ3Kq3B177m1DCyptdz3qm+fNtwccbNxKgdraQ+5933o24cNdybu2biHBiwiP8y6HXnTt7+8Cnevz8YBi5l1q3d9+6fyStxs3DQcx1nmTLNu8vZJmdLROGA5z7qlom/fjLiSTjdgGelB3n5O3JSABR1107dvEwesa+MHReZgRcbb/yqO4yx1AAAAAH6xBwcCAAAAAED+r42gqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqirtwSEBAAAAgKD/r81+AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYALG6vVOk3uGfAAAAABJRU5ErkJggg==)

> [!NOTE]
> このシナリオでは、基盤となる認証可能なモデルへの変換レイヤーとして OAuth を使用しているだけです。スコープなど、OAuth の多くの側面を無視しています。

<!-- #### Using an Existing Passport Installation -->
#### Using an Existing Passport Installation

<!-- If your application is already using Laravel Passport, Laravel MCP should work seamlessly within your existing Passport installation, but custom scopes aren't currently supported as OAuth is primarily used as a translation layer to the underlying authenticatable model. -->
アプリケーションがすでに Laravel Passport を使用している場合、Laravel MCP は既存の Passport インストール内でシームレスに動作するはずですが、OAuth は主に基盤となる認証可能なモデルへの変換レイヤーとして使用されるため、カスタム スコープは現在サポートされていません。

<!-- Laravel MCP, via the `Mcp::oauthRoutes` method discussed above, adds, advertises, and uses a single `mcp:use` scope. -->
Laravel MCP は、上で説明した `Mcp::oauthRoutes` メソッドを介して、単一の `mcp:use` スコープを追加、アドバタイズ、および使用します。

<!-- #### Passport vs. Sanctum -->
#### Passport vs. Sanctum

<!-- OAuth2.1 is the documented authentication mechanism in the Model Context Protocol specification, and is the most widely supported among MCP clients. For that reason, we recommend using Passport when possible. -->
OAuth2.1 はモデル コンテキスト プロトコル仕様で文書化された認証メカニズムであり、MCP クライアント間で最も広くサポートされています。そのため、可能な限りPassportを使用することをお勧めします。

<!-- If your application is already using [Sanctum](/docs/13.x/sanctum) then adding Passport may be cumbersome. In this instance, we recommend using Sanctum without Passport until you have a clear, necessary requirement to use an MCP client that only supports OAuth. -->
アプリケーションがすでに [Sanctum](/docs/13.x/sanctum) を使用している場合、Passport の追加は面倒な場合があります。この場合、OAuth のみをサポートする MCP クライアントを使用するための明確な必要な要件が得られるまで、Passport なしで Sanctum を使用することをお勧めします。

<a name="sanctum"></a>
<!-- ### Sanctum -->
### Sanctum

<!-- If you would like to protect your MCP server using [Sanctum](/docs/13.x/sanctum), simply add Sanctum's authentication middleware to your server in your `routes/ai.php` file. Then, ensure your MCP clients provide an `Authorization: Bearer <token>` header to ensure successful authentication: -->
[Sanctum](/docs/13.x/sanctum) を使用して MCP サーバーを保護したい場合は、`routes/ai.php` ファイルで Sanctum の認証ミドルウェアをサーバーに追加するだけです。次に、認証が成功するように、MCP クライアントが `Authorization: Bearer <token>` ヘッダーを提供していることを確認します。

```php
use App\Mcp\Servers\WeatherExample;
use Laravel\Mcp\Facades\Mcp;

Mcp::web('/mcp/demo', WeatherExample::class)
    ->middleware('auth:sanctum');
```

<a name="custom-mcp-authentication"></a>
<!-- #### Custom MCP Authentication -->
#### Custom MCP Authentication

<!-- If your application issues its own custom API tokens, you may authenticate your MCP server by assigning any middleware you wish to your `Mcp::web` routes. Your custom middleware can inspect the `Authorization` header manually to authenticate the incoming MCP request. -->
アプリケーションが独自のカスタム API トークンを発行する場合、必要なミドルウェアを `Mcp::web` ルートに割り当てることで、MCP サーバーを認証できます。カスタム ミドルウェアは、`Authorization` ヘッダーを手動で検査して、受信 MCP リクエストを認証できます。

<a name="authorization"></a>
<!-- ## Authorization -->
## Authorization

<!-- You may access the currently authenticated user via the `$request->user()` method, allowing you to perform [authorization checks](/docs/13.x/authorization) within your MCP tools and resources: -->
`$request->user()` メソッドを介して現在認証されているユーザーにアクセスすると、MCP ツールおよびリソース内で [authorization checks](/docs/13.x/authorization) を実行できるようになります。

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

<a name="client"></a>
<!-- ## MCP Client -->
## MCP Client

<!-- In addition to building servers, Laravel MCP includes a client for connecting to other MCP servers, whether first-party or third-party. The client lets your application discover and call the tools exposed by an MCP server, which is especially useful for giving your [AI agents](/docs/13.x/ai-sdk#mcp-tools) access to capabilities provided by external MCP servers. -->
Laravel MCP は、サーバーの構築に加えて、ファーストパーティかサードパーティかを問わず、他の MCP サーバーへ接続するためのクライアントも備えています。クライアントを使うと、アプリケーションは MCP サーバーが公開するツールを検出して呼び出せます。これは、[AI agents](/docs/13.x/ai-sdk#mcp-tools) に外部 MCP サーバーが提供する機能へのアクセスを与えたい場合に特に便利です。

<a name="client-connecting"></a>
<!-- ### Connecting to Servers -->
### Connecting to Servers

<!-- You may connect to an HTTP-accessible MCP server using the `Client::web` method, passing the server's URL: -->
HTTP でアクセスできる MCP サーバーへは、サーバーの URL を渡して `Client::web` メソッドで接続できます。

```php
use Laravel\Mcp\Client;

$client = Client::web('https://mcp.example.com');
```

<!-- To connect to a local MCP server that runs as a command, use the `Client::local` method, providing the command and any arguments needed to start the server: -->
コマンドとして実行されるローカルの MCP サーバーへ接続するには、`Client::local` メソッドを使用し、サーバーを起動するためのコマンドと必要な引数を指定します。

```php
use Laravel\Mcp\Client;

$client = Client::local('php', ['artisan', 'mcp:start']);
```

<!-- The client connects lazily, automatically establishing the connection the first time you list or call tools. If you need to manage the connection manually, you may use the `connect`, `connected`, `ping`, and `disconnect` methods: -->
クライアントは遅延的に接続し、最初にツールを一覧表示または呼び出したときに自動的に接続を確立します。接続を手動で管理する必要がある場合は、`connect`、`connected`、`ping`、`disconnect` メソッドを使用できます。

```php
$client->connect();

$client->ping();

if ($client->connected()) {
    // ...
}

$client->disconnect();
```

<!-- You may customize the request timeout using the `withTimeout` method: -->
`withTimeout` メソッドを使用して、リクエストのタイムアウトをカスタマイズできます。

```php
$client = Client::web('https://mcp.example.com')->withTimeout(30);
```

<a name="named-clients"></a>
<!-- ### Named Clients -->
### Named Clients

<!-- Instead of constructing a client each time you need it, you may register reusable, named clients. This is typically done in the `boot` method of a service provider using the `Mcp` facade: -->
必要になるたびにクライアントを構築する代わりに、再利用可能な名前付きクライアントを登録できます。これは通常、`Mcp` ファサードを使用してサービスプロバイダの `boot` メソッド内で行います。

```php
use Laravel\Mcp\Client;
use Laravel\Mcp\Facades\Mcp;

Mcp::registerClient('github', fn () => Client::web('https://mcp.example.com'));
```

<!-- Once registered, you may resolve the client anywhere in your application by name: -->
登録すると、アプリケーションのどこからでも名前でクライアントを解決できます。

```php
use Laravel\Mcp\Facades\Mcp;

$client = Mcp::client('github');
```

<!-- Named clients are resolved once per request and automatically disconnected at the end of the request lifecycle. -->
名前付きクライアントはリクエストごとに一度だけ解決され、リクエストのライフサイクルの終了時に自動的に切断されます。

<a name="client-authentication"></a>
<!-- ### Client Authentication -->
### Client Authentication

<!-- To connect to a web MCP server that is protected by a bearer token, use the `withToken` method. You may pass a token string or a closure that lazily resolves the token: -->
ベアラートークンで保護されたウェブ MCP サーバーへ接続するには、`withToken` メソッドを使用します。トークン文字列、またはトークンを遅延的に解決するクロージャを渡せます。

```php
use Illuminate\Support\Facades\Auth;
use Laravel\Mcp\Client;

$client = Client::web('https://mcp.example.com')->withToken($token);

$client = Client::web('https://mcp.example.com')->withToken(
    fn () => Auth::user()->mcpToken(),
);
```

<!-- For servers protected by [OAuth 2.1](#oauth), configure the client using the `withOAuth` method. This is the client-side counterpart to protecting your own servers with OAuth: -->
[OAuth 2.1](#oauth) で保護されたサーバーの場合は、`withOAuth` メソッドを使用してクライアントを構成します。これは、自身のサーバーを OAuth で保護する処理のクライアント側に対応するものです。

```php
use Laravel\Mcp\Client;
use Laravel\Mcp\Facades\Mcp;

Mcp::registerClient('github', fn () => Client::web('https://mcp.example.com')->withOAuth(
    clientId: config('services.github_mcp.client_id'),
    clientSecret: config('services.github_mcp.client_secret'),
));
```

> [!NOTE]
> MCP サーバーが [dynamic client registration](https://datatracker.ietf.org/doc/html/rfc7591) をサポートしている場合は `clientId` と `clientSecret` 引数を省略でき、その場合クライアントは自動的に自身を登録します。

<!-- Next, register the OAuth routes for the named client in your `routes/ai.php` file using the `oAuthRoutesFor` method. The closure you provide receives the client name and resulting `TokenSet` after the authorization code has been exchanged for an access token: -->
次に、`oAuthRoutesFor` メソッドを使用して、名前付きクライアントの OAuth ルートを `routes/ai.php` ファイルに登録します。指定したクロージャは、認可コードがアクセストークンと交換された後に、クライアント名と生成された `TokenSet` を受け取ります。

```php
use Illuminate\Support\Facades\Auth;
use Laravel\Mcp\Client\OAuth\TokenSet;
use Laravel\Mcp\Facades\Mcp;

Mcp::oAuthRoutesFor('github', function (string $client, TokenSet $token) {
    Auth::user()->update([
        'github_mcp_token' => $token->accessToken,
    ]);

    return redirect('/dashboard');
});
```

<!-- This registers two named routes: a connect route (`mcp.oauth.{client}.connect`) that redirects the user to the authorization server, and a callback route (`mcp.oauth.{client}.callback`) that exchanges the authorization code and invokes your handler. Both routes use the `web` middleware group by default, which you may override using the `middleware` argument. -->
これにより、2 つの名前付きルートが登録されます。ユーザーを認可サーバーへリダイレクトする接続ルート (`mcp.oauth.{client}.connect`) と、認可コードを交換してハンドラを呼び出すコールバックルート (`mcp.oauth.{client}.callback`) です。どちらのルートもデフォルトで `web` ミドルウェアグループを使用し、`middleware` 引数で上書きできます。

<!-- To begin the authorization flow, redirect the user to the connect route: -->
認可フローを開始するには、ユーザーを接続ルートへリダイレクトします。

```php
return redirect()->route('mcp.oauth.github.connect');
```

<a name="client-tools"></a>
<!-- ### Tools -->
### Tools

<!-- You may retrieve the tools exposed by an MCP server using the `tools` method, which returns a collection of tools keyed by name: -->
MCP サーバーが公開するツールは、`tools` メソッドを使用して取得できます。このメソッドは名前をキーとするツールのコレクションを返します。

```php
use Laravel\Mcp\Facades\Mcp;

$tools = Mcp::client('github')->tools();

foreach ($tools as $tool) {
    $tool->name;
    $tool->title;
    $tool->description;
    $tool->inputSchema;
}
```

<!-- The client automatically paginates through all available tools. You may limit the number of tools returned using the `limit` argument: -->
クライアントは利用可能なすべてのツールを自動的にページネーションします。`limit` 引数を使用して、返されるツールの数を制限できます。

```php
$tools = Mcp::client('github')->tools(limit: 10);
```

<!-- To invoke a tool, use the `callTool` method, passing the tool name and an array of arguments. The returned `ToolResult` instance exposes the tool response: -->
ツールを呼び出すには、`callTool` メソッドにツール名と引数の配列を渡します。返される `ToolResult` インスタンスからツールの応答にアクセスできます。

```php
use Laravel\Mcp\Facades\Mcp;

$result = Mcp::client('github')->callTool('current-weather', [
    'location' => 'New York',
]);

$result->text(); // The text content of the response...
(string) $result; // Equivalent to calling text()...
$result->isError; // Whether the tool reported an error...
$result->structuredContent;  // Structured content, if any...
```

<!-- Alternatively, you may call a tool directly from a listed tool instance: -->
あるいは、一覧表示したツールインスタンスから直接ツールを呼び出すこともできます。

```php
$tools = Mcp::client('github')->tools();

$result = $tools['current-weather']->call([
    'location' => 'New York',
]);
```

<!-- If you are building agents with the [Laravel AI SDK](/docs/13.x/ai-sdk), you may also provide tools from an MCP client directly to an agent, allowing the model to call them while responding to a prompt. See the [MCP Tools](/docs/13.x/ai-sdk#mcp-tools) section of the AI SDK documentation for more information. -->
[Laravel AI SDK](/docs/13.x/ai-sdk) でエージェントを構築している場合は、MCP クライアントのツールをエージェントへ直接提供することもでき、モデルがプロンプトに応答しながらそれらを呼び出せます。詳細については、AI SDK ドキュメントの [MCP Tools](/docs/13.x/ai-sdk#mcp-tools) セクションを参照してください。

<a name="client-prompts"></a>
<!-- ### Prompts -->
### Prompts

<!-- You may retrieve the prompts exposed by an MCP server using the `prompts` method, which returns a collection of prompts keyed by name: -->
MCP サーバーが公開するプロンプトは、`prompts` メソッドを使用して取得できます。このメソッドは名前をキーとするプロンプトのコレクションを返します。

```php
use Laravel\Mcp\Facades\Mcp;

$prompts = Mcp::client('github')->prompts();

foreach ($prompts as $prompt) {
    $prompt->name;
    $prompt->title;
    $prompt->description;
    $prompt->arguments;
}
```

<!-- The client automatically paginates through all available prompts. You may limit the number of prompts returned using the `limit` argument: -->
クライアントは利用可能なすべてのプロンプトを自動的にページネーションします。`limit` 引数を使用して、返されるプロンプトの数を制限できます。

```php
$prompts = Mcp::client('github')->prompts(limit: 10);
```

<!-- To retrieve a prompt, use the `getPrompt` method, passing the prompt name and an array of arguments. The returned `PromptResult` instance exposes the generated messages: -->
プロンプトを取得するには、`getPrompt` メソッドにプロンプト名と引数の配列を渡します。返される `PromptResult` インスタンスから生成されたメッセージにアクセスできます。

```php
use Laravel\Mcp\Facades\Mcp;

$result = Mcp::client('github')->getPrompt('describe-weather', [
    'location' => 'New York',
]);

$result->text(); // The text content of the messages...
(string) $result; // Equivalent to calling text()...
$result->messages; // The raw messages returned by the prompt...
$result->description; // The prompt description, if any...
```

<a name="client-resources"></a>
<!-- ### Resources -->
### Resources

<!-- You may retrieve the resources exposed by an MCP server using the `resources` method, which returns a collection of resources keyed by URI: -->
MCP サーバーが公開するリソースは、`resources` メソッドを使用して取得できます。このメソッドは URI をキーとするリソースのコレクションを返します。

```php
use Laravel\Mcp\Facades\Mcp;

$resources = Mcp::client('github')->resources();

foreach ($resources as $resource) {
    $resource->uri;
    $resource->name;
    $resource->title;
    $resource->description;
    $resource->mimeType;
    $resource->size;
}
```

<!-- The client automatically paginates through all available resources. You may limit the number of resources returned using the `limit` argument: -->
クライアントは利用可能なすべてのリソースを自動的にページネーションします。`limit` 引数を使用して、返されるリソースの数を制限できます。

```php
$resources = Mcp::client('github')->resources(limit: 10);
```

<!-- To read a resource, use the `readResource` method, passing the resource URI. The returned `ResourceReadResult` instance exposes the resource content: -->
リソースを読み取るには、`readResource` メソッドにリソースの URI を渡します。返される `ResourceReadResult` インスタンスからリソースのコンテンツにアクセスできます。

```php
use Laravel\Mcp\Facades\Mcp;

$result = Mcp::client('github')->readResource('weather://guidelines');

$result->content(); // The content of the resource, decoding base64 blobs as needed...
(string) $result; // Equivalent to calling content()...
$result->mimeType(); // The MIME type of the resource, if any...
$result->contents; // The raw contents returned by the resource...
```

<a name="testing-servers"></a>
<!-- ## Testing Servers -->
## Testing Servers

<!-- You may test your MCP servers using the built-in MCP Inspector or by writing unit tests. -->
組み込みの MCP インスペクターを使用するか、単体テストを作成することによって、MCP サーバーをテストできます。

<a name="mcp-inspector"></a>
<!-- ### MCP Inspector -->
### MCP Inspector

<!-- The [MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector) is an interactive tool for testing and debugging your MCP servers. Use it to connect to your server, verify authentication, and try out tools, resources, and prompts. -->
[MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector) は、MCP サーバーをテストおよびデバッグするための対話型ツールです。これを使用してサーバーに接続し、認証を確認し、ツール、リソース、プロンプトを試します。

<!-- You may run the inspector for any registered server: -->
登録されている任意のサーバーに対してインスペクタを実行できます。

```shell
# Web server...
php artisan mcp:inspector mcp/weather

# Local server named "weather"...
php artisan mcp:inspector weather
```

<!-- This command launches the MCP Inspector and provides the client settings that you may copy into your MCP client to ensure everything is configured correctly. If your web server is protected by an authentication middleware, make sure to include the required headers, such as an `Authorization` bearer token, when connecting. -->
このコマンドは MCP インスペクターを起動し、すべてが正しく構成されていることを確認するために MCP クライアントにコピーできるクライアント設定を提供します。 Web サーバーが認証ミドルウェアによって保護されている場合は、接続時に `Authorization` ベアラー トークンなどの必要なヘッダーを必ず含めてください。

<a name="unit-tests"></a>
<!-- ### Unit Tests -->
### Unit Tests

<!-- You may write unit tests for your MCP servers, tools, resources, and prompts. -->
MCP サーバー、ツール、リソース、プロンプトの単体テストを作成できます。

<!-- To get started, create a new test case and invoke the desired primitive on the server that registers it. For example, to test a tool on the `WeatherServer`: -->
まず、新しいテスト ケースを作成し、それを登録するサーバー上で目的のプリミティブを呼び出します。たとえば、`WeatherServer` でツールをテストするには:

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

<!-- Similarly, you may test prompts and resources: -->
同様に、プロンプトとリソースをテストできます。

```php
$response = WeatherServer::prompt(...);
$response = WeatherServer::resource(...);
```

<!-- You may also act as an authenticated user by chaining the `actingAs` method before invoking the primitive: -->
プリミティブを呼び出す前に `actingAs` メソッドをチェーンすることで、認証されたユーザーとして動作することもできます。

```php
$response = WeatherServer::actingAs($user)->tool(...);
```

<!-- Once you receive the response, you may use various assertion methods to verify the content and status of the response. -->
応答を受信したら、さまざまなアサーション メソッドを使用して、応答の内容とステータスを確認できます。

<!-- You may assert that a response is successful using the `assertOk` method. This checks that the response does not have any errors: -->
`assertOk` メソッドを使用して、応答が成功したことをアサートできます。これにより、応答にエラーがないことがチェックされます。

```php
$response->assertOk();
```

<!-- You may assert that a response contains specific text using the `assertSee` method: -->
`assertSee` メソッドを使用して、応答に特定のテキストが含まれていることをアサートできます。

```php
$response->assertSee('The current weather in New York City is 72°F and sunny.');
```

<!-- You may assert that a response contains an error using the `assertHasErrors` method: -->
`assertHasErrors` メソッドを使用して、応答にエラーが含まれていることをアサートできます。

```php
$response->assertHasErrors();

$response->assertHasErrors([
    'Something went wrong.',
]);
```

<!-- You may assert that a response does not contain an error using the `assertHasNoErrors` method: -->
`assertHasNoErrors` メソッドを使用して、応答にエラーが含まれていないことを主張できます。

```php
$response->assertHasNoErrors();
```

<!-- You may assert that a response contains specific metadata using the `assertName()`, `assertTitle()`, and `assertDescription()` methods: -->
`assertName()`、`assertTitle()`、および `assertDescription()` メソッドを使用して、応答に特定のメタデータが含まれていることをアサートできます。

```php
$response->assertName('current-weather');
$response->assertTitle('Current Weather Tool');
$response->assertDescription('Fetches the current weather forecast for a specified location.');
```

<!-- You may assert that notifications were sent using the `assertSentNotification` and `assertNotificationCount` methods: -->
通知が `assertSentNotification` および `assertNotificationCount` メソッドを使用して送信されたと主張できます。

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

<!-- Finally, if you wish to inspect the raw response content, you may use the `dd` or `dump` methods to output the response for debugging purposes: -->
最後に、生の応答コンテンツを検査したい場合は、`dd` メソッドまたは `dump` メソッドを使用して、デバッグ目的で応答を出力できます。

```php
$response->dd();
$response->dump();
```
