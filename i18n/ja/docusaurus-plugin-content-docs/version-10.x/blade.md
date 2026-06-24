<!-- # Blade Templates -->
# Blade Templates

- [Introduction](#introduction)
    - [Supercharging Blade With Livewire](#supercharging-blade-with-livewire)
- [Displaying Data](#displaying-data)
    - [HTML Entity Encoding](#html-entity-encoding)
    - [Blade and JavaScript Frameworks](#blade-and-javascript-frameworks)
- [Blade Directives](#blade-directives)
    - [If Statements](#if-statements)
    - [Switch Statements](#switch-statements)
    - [Loops](#loops)
    - [The Loop Variable](#the-loop-variable)
    - [Conditional Classes](#conditional-classes)
    - [Additional Attributes](#additional-attributes)
    - [Including Subviews](#including-subviews)
    - [The `@once` Directive](#the-once-directive)
    - [Raw PHP](#raw-php)
    - [Comments](#comments)
- [Components](#components)
    - [Rendering Components](#rendering-components)
    - [Passing Data to Components](#passing-data-to-components)
    - [Component Attributes](#component-attributes)
    - [Reserved Keywords](#reserved-keywords)
    - [Slots](#slots)
    - [Inline Component Views](#inline-component-views)
    - [Dynamic Components](#dynamic-components)
    - [Manually Registering Components](#manually-registering-components)
- [Anonymous Components](#anonymous-components)
    - [Anonymous Index Components](#anonymous-index-components)
    - [Data Properties / Attributes](#data-properties-attributes)
    - [Accessing Parent Data](#accessing-parent-data)
    - [Anonymous Components Paths](#anonymous-component-paths)
- [Building Layouts](#building-layouts)
    - [Layouts Using Components](#layouts-using-components)
    - [Layouts Using Template Inheritance](#layouts-using-template-inheritance)
- [Forms](#forms)
    - [CSRF Field](#csrf-field)
    - [Method Field](#method-field)
    - [Validation Errors](#validation-errors)
- [Stacks](#stacks)
- [Service Injection](#service-injection)
- [Rendering Inline Blade Templates](#rendering-inline-blade-templates)
- [Rendering Blade Fragments](#rendering-blade-fragments)
- [Extending Blade](#extending-blade)
    - [Custom Echo Handlers](#custom-echo-handlers)
    - [Custom If Statements](#custom-if-statements)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Blade is the simple, yet powerful templating engine that is included with Laravel. Unlike some PHP templating engines, Blade does not restrict you from using plain PHP code in your templates. In fact, all Blade templates are compiled into plain PHP code and cached until they are modified, meaning Blade adds essentially zero overhead to your application. Blade template files use the `.blade.php` file extension and are typically stored in the `resources/views` directory. -->
Blade は、Laravel に含まれるシンプルかつ強力なテンプレート エンジンです。一部の PHP テンプレート エンジンとは異なり、Blade では、テンプレート内でプレーンな PHP コードを使用することが制限されません。実際、すべての Blade テンプレートはプレーンな PHP コードにコンパイルされ、変更されるまでキャッシュされます。つまり、Blade はアプリケーションに本質的にオーバーヘッドを追加しません。Blade テンプレート ファイルは、`.blade.php` ファイル拡張子を使用し、通常は `resources/views` ディレクトリに保存されます。

<!-- Blade views may be returned from routes or controllers using the global `view` helper. Of course, as mentioned in the documentation on [views](/docs/10.x/views), data may be passed to the Blade view using the `view` helper's second argument: -->
Blade ビューは、グローバル `view` ヘルパを使用してルートまたはコントローラから返される場合があります。もちろん、[views](/docs/10.x/views) のドキュメントで説明されているように、`view` ヘルパの 2 番目の引数を使用してデータをBlade ビューに渡すこともできます。

```
Route::get('/', function () {
    return view('greeting', ['name' => 'Finn']);
});
```

<a name="supercharging-blade-with-livewire"></a>
<!-- ### Supercharging Blade With Livewire -->
### Supercharging Blade With Livewire

<!-- Want to take your Blade templates to the next level and build dynamic interfaces with ease? Check out [Laravel Livewire](https://livewire.laravel.com). Livewire allows you to write Blade components that are augmented with dynamic functionality that would typically only be possible via frontend frameworks like React or Vue, providing a great approach to building modern, reactive frontends without the complexities, client-side rendering, or build steps of many JavaScript frameworks. -->
Blade テンプレートを次のレベルに引き上げて、動的なインターフェイスを簡単に構築したいですか? [Laravel Livewire](https://livewire.laravel.com) をチェックしてください。 Livewire を使用すると、通常は React や Vue などのフロントエンド フレームワークを介してのみ可能となる動的機能で拡張された Blade コンポーネントを作成でき、多くの JavaScript フレームワークの複雑さ、クライアント側のレンダリング、ビルド手順を必要とせずに、最新のリアクティブ フロントエンドを構築するための優れたアプローチを提供します。

<a name="displaying-data"></a>
<!-- ## Displaying Data -->
## Displaying Data

<!-- You may display data that is passed to your Blade views by wrapping the variable in curly braces. For example, given the following route: -->
変数を中括弧で囲むことにより、Blade ビューに渡されるデータを表示できます。たとえば、次のルートがあるとします。

```
Route::get('/', function () {
    return view('welcome', ['name' => 'Samantha']);
});
```

<!-- You may display the contents of the `name` variable like so: -->
次のように `name` 変数の内容を表示できます。

```blade
Hello, {{ $name }}.
```

> [!NOTE]
> Blade の `{{ }}` エコー ステートメントは、PHP の `htmlspecialchars` 関数を通じて自動的に送信され、XSS 攻撃を防ぎます。

<!-- You are not limited to displaying the contents of the variables passed to the view. You may also echo the results of any PHP function. In fact, you can put any PHP code you wish inside of a Blade echo statement: -->
ビューに渡された変数の内容を表示することに限定されません。任意の PHP 関数の結果をエコーすることもできます。実際、Blade echo ステートメント内に任意の PHP コードを含めることができます。

```blade
The current UNIX timestamp is {{ time() }}.
```

<a name="html-entity-encoding"></a>
<!-- ### HTML Entity Encoding -->
### HTML Entity Encoding

<!-- By default, Blade (and the Laravel `e` function) will double encode HTML entities. If you would like to disable double encoding, call the `Blade::withoutDoubleEncoding` method from the `boot` method of your `AppServiceProvider`: -->
デフォルトでは、Blade (および Laravel `e` 関数) は HTML エンティティを二重エンコードします。二重エンコードを無効にしたい場合は、`AppServiceProvider` の `boot` メソッドから `Blade::withoutDoubleEncoding` メソッドを呼び出します。

```
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Blade;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Blade::withoutDoubleEncoding();
    }
}
```

<a name="displaying-unescaped-data"></a>
<!-- #### Displaying Unescaped Data -->
#### Displaying Unescaped Data

<!-- By default, Blade `{{ }}` statements are automatically sent through PHP's `htmlspecialchars` function to prevent XSS attacks. If you do not want your data to be escaped, you may use the following syntax: -->
デフォルトでは、Bladeの `{{ }}` ステートメントは、XSS 攻撃を防ぐために、PHP の `htmlspecialchars` 関数を通じて自動的に送信されます。データをエスケープしたくない場合は、次の構文を使用できます。

```blade
Hello, {!! $name !!}.
```

> [!WARNING]
> アプリケーションのユーザーが提供したコンテンツをエコーする場合は、十分に注意してください。ユーザーが指定したデータを表示するときに XSS 攻撃を防ぐには、通常、エスケープされた二重中括弧構文を使用する必要があります。

<a name="blade-and-javascript-frameworks"></a>
<!-- ### Blade and JavaScript Frameworks -->
### Blade and JavaScript Frameworks

<!-- Since many JavaScript frameworks also use "curly" braces to indicate a given expression should be displayed in the browser, you may use the `@` symbol to inform the Blade rendering engine an expression should remain untouched. For example: -->
多くの JavaScript フレームワークでも、特定の式をブラウザーに表示する必要があることを示すために「中括弧」を使用するため、`@` シンボルを使用して、式をそのままにしておく必要があることを Blade レンダリング エンジンに通知できます。例えば：

```blade
<h1>Laravel</h1>

Hello, @{{ name }}.
```

<!-- In this example, the `@` symbol will be removed by Blade; however, `{{ name }}` expression will remain untouched by the Blade engine, allowing it to be rendered by your JavaScript framework. -->
この例では、`@` シンボルが Blade によって削除されます。ただし、`{{ name }}` 式は Blade エンジンによって変更されないため、JavaScript フレームワークによってレンダリングできます。

<!-- The `@` symbol may also be used to escape Blade directives: -->
`@` シンボルは、Blade ディレクティブをエスケープするために使用することもできます。

```blade
{{-- Blade template --}}
@@if()

<!-- HTML output -->
@if()
```

<a name="rendering-json"></a>
<!-- #### Rendering JSON -->
#### Rendering JSON

<!-- Sometimes you may pass an array to your view with the intention of rendering it as JSON in order to initialize a JavaScript variable. For example: -->
JavaScript 変数を初期化するために、配列を JSON としてレンダリングする目的でビューに配列を渡すことがあります。例えば：

```blade
<script>
    var app = <?php echo json_encode($array); ?>;
</script>
```

<!-- However, instead of manually calling `json_encode`, you may use the `Illuminate\Support\Js::from` method directive. The `from` method accepts the same arguments as PHP's `json_encode` function; however, it will ensure that the resulting JSON is properly escaped for inclusion within HTML quotes. The `from` method will return a string `JSON.parse` JavaScript statement that will convert the given object or array into a valid JavaScript object: -->
ただし、`json_encode` を手動で呼び出す代わりに、`Illuminate\Support\Js::from` メソッド ディレクティブを使用することもできます。 `from` メソッドは、PHP の `json_encode` 関数と同じ引数を受け入れます。ただし、結果の JSON が HTML 引用符内に含められるように適切にエスケープされることが保証されます。 `from` メソッドは、指定されたオブジェクトまたは配列を有効な JavaScript オブジェクトに変換する文字列 `JSON.parse` JavaScript ステートメントを返します。

```blade
<script>
    var app = {{ Illuminate\Support\Js::from($array) }};
</script>
```

<!-- The latest versions of the Laravel application skeleton include a `Js` facade, which provides convenient access to this functionality within your Blade templates: -->
Laravel アプリケーション スケルトンの最新バージョンには、Blade テンプレート内のこの機能への便利なアクセスを提供する `Js` ファサードが含まれています。

```blade
<script>
    var app = {{ Js::from($array) }};
</script>
```

> [!WARNING]
> 既存の変数を JSON としてレンダリングする場合は、`Js::from` メソッドのみを使用してください。 Blade テンプレートは正規表現に基づいており、複雑な表現をディレクティブに渡そうとすると、予期しないエラーが発生する可能性があります。

<a name="the-at-verbatim-directive"></a>
<!-- #### The `@verbatim` Directive -->
#### The `@verbatim` Directive

<!-- If you are displaying JavaScript variables in a large portion of your template, you may wrap the HTML in the `@verbatim` directive so that you do not have to prefix each Blade echo statement with an `@` symbol: -->
テンプレートの大部分で JavaScript 変数を表示している場合は、HTML を `@verbatim` ディレクティブでラップすると、各 Blade echo ステートメントの前に `@` シンボルを付ける必要がなくなります。

```blade
@verbatim
    <div class="container">
        Hello, {{ name }}.
    </div>
@endverbatim
```

<a name="blade-directives"></a>
<!-- ## Blade Directives -->
## Blade Directives

<!-- In addition to template inheritance and displaying data, Blade also provides convenient shortcuts for common PHP control structures, such as conditional statements and loops. These shortcuts provide a very clean, terse way of working with PHP control structures while also remaining familiar to their PHP counterparts. -->
Blade は、テンプレートの継承とデータの表示に加えて、条件ステートメントやループなどの一般的な PHP 制御構造の便利なショートカットも提供します。これらのショートカットは、PHP の制御構造を操作するための非常にクリーンで簡潔な方法を提供すると同時に、PHP の対応するものにとっても馴染みのあるものです。

<a name="if-statements"></a>
<!-- ### If Statements -->
### If Statements

<!-- You may construct `if` statements using the `@if`, `@elseif`, `@else`, and `@endif` directives. These directives function identically to their PHP counterparts: -->
`if` ステートメントは、`@if`、`@elseif`、`@else`、および `@endif` ディレクティブを使用して作成できます。これらのディレクティブは、対応する PHP ディレクティブと同様に機能します。

```blade
@if (count($records) === 1)
    I have one record!
@elseif (count($records) > 1)
    I have multiple records!
@else
    I don't have any records!
@endif
```

<!-- For convenience, Blade also provides an `@unless` directive: -->
便宜上、Blade には `@unless` ディレクティブも用意されています。

```blade
@unless (Auth::check())
    You are not signed in.
@endunless
```

<!-- In addition to the conditional directives already discussed, the `@isset` and `@empty` directives may be used as convenient shortcuts for their respective PHP functions: -->
すでに説明した条件付きディレクティブに加えて、`@isset` および `@empty` ディレクティブは、それぞれの PHP 関数の便利なショートカットとして使用できます。

```blade
@isset($records)
    // $records is defined and is not null...
@endisset

@empty($records)
    // $records is "empty"...
@endempty
```

<a name="authentication-directives"></a>
<!-- #### Authentication Directives -->
#### Authentication Directives

<!-- The `@auth` and `@guest` directives may be used to quickly determine if the current user is [authenticated](/docs/10.x/authentication) or is a guest: -->
`@auth` および `@guest` ディレクティブを使用すると、現在のユーザーが [authenticated](/docs/10.x/authentication) であるかゲストであるかを迅速に判断できます。

```blade
@auth
    // The user is authenticated...
@endauth

@guest
    // The user is not authenticated...
@endguest
```

<!-- If needed, you may specify the authentication guard that should be checked when using the `@auth` and `@guest` directives: -->
必要に応じて、`@auth` および `@guest` ディレクティブを使用するときにチェックする必要がある認証ガードを指定できます。

```blade
@auth('admin')
    // The user is authenticated...
@endauth

@guest('admin')
    // The user is not authenticated...
@endguest
```

<a name="environment-directives"></a>
<!-- #### Environment Directives -->
#### Environment Directives

<!-- You may check if the application is running in the production environment using the `@production` directive: -->
`@production` ディレクティブを使用して、アプリケーションが運用環境で実行されているかどうかを確認できます。

```blade
@production
    // Production specific content...
@endproduction
```

<!-- Or, you may determine if the application is running in a specific environment using the `@env` directive: -->
または、`@env` ディレクティブを使用して、アプリケーションが特定の環境で実行されているかどうかを確認することもできます。

```blade
@env('staging')
    // The application is running in "staging"...
@endenv

@env(['staging', 'production'])
    // The application is running in "staging" or "production"...
@endenv
```

<a name="section-directives"></a>
<!-- #### Section Directives -->
#### Section Directives

<!-- You may determine if a template inheritance section has content using the `@hasSection` directive: -->
`@hasSection` ディレクティブを使用して、テンプレート継承セクションにコンテンツがあるかどうかを判断できます。

```blade
@hasSection('navigation')
    <div class="pull-right">
        @yield('navigation')
    </div>

    <div class="clearfix"></div>
@endif
```

<!-- You may use the `sectionMissing` directive to determine if a section does not have content: -->
`sectionMissing` ディレクティブを使用して、セクションにコンテンツがないかどうかを判断できます。

```blade
@sectionMissing('navigation')
    <div class="pull-right">
        @include('default-navigation')
    </div>
@endif
```

<a name="session-directives"></a>
<!-- #### Session Directives -->
#### Session Directives

<!-- The `@session` directive may be used to determine if a [session](/docs/10.x/session) value exists. If the session value exists, the template contents within the `@session` and `@endsession` directives will be evaluated. Within the `@session` directive's contents, you may echo the `$value` variable to display the session value: -->
`@session` ディレクティブは、[session](/docs/10.x/session) 値が存在するかどうかを判断するために使用できます。セッション値が存在する場合、`@session` および `@endsession` ディレクティブ内のテンプレートの内容が評価されます。 `@session` ディレクティブの内容内で、`$value` 変数をエコーし​​てセッション値を表示できます。

```blade
@session('status')
    <div class="p-4 bg-green-100">
        {{ $value }}
    </div>
@endsession
```

<a name="switch-statements"></a>
<!-- ### Switch Statements -->
### Switch Statements

<!-- Switch statements can be constructed using the `@switch`, `@case`, `@break`, `@default` and `@endswitch` directives: -->
switch ステートメントは、`@switch`、`@case`、`@break`、`@default`、および `@endswitch` ディレクティブを使用して構築できます。

```blade
@switch($i)
    @case(1)
        First case...
        @break

    @case(2)
        Second case...
        @break

    @default
        Default case...
@endswitch
```

<a name="loops"></a>
<!-- ### Loops -->
### Loops

<!-- In addition to conditional statements, Blade provides simple directives for working with PHP's loop structures. Again, each of these directives functions identically to their PHP counterparts: -->
条件文に加えて、Blade は PHP のループ構造を操作するための単純なディレクティブを提供します。繰り返しますが、これらの各ディレクティブは、対応する PHP ディレクティブと同様に機能します。

```blade
@for ($i = 0; $i < 10; $i++)
    The current value is {{ $i }}
@endfor

@foreach ($users as $user)
    <p>This is user {{ $user->id }}</p>
@endforeach

@forelse ($users as $user)
    <li>{{ $user->name }}</li>
@empty
    <p>No users</p>
@endforelse

@while (true)
    <p>I'm looping forever.</p>
@endwhile
```

> [!NOTE]
> `foreach` ループを反復しているときに、[loop variable](#the-loop-variable) を使用して、ループの最初の反復にいるか最後の反復にいるかなど、ループに関する貴重な情報を取得できます。

<!-- When using loops you may also skip the current iteration or end the loop using the `@continue` and `@break` directives: -->
ループを使用する場合、`@continue` および `@break` ディレクティブを使用して、現在の反復をスキップしたり、ループを終了したりすることもできます。

```blade
@foreach ($users as $user)
    @if ($user->type == 1)
        @continue
    @endif

    <li>{{ $user->name }}</li>

    @if ($user->number == 5)
        @break
    @endif
@endforeach
```

<!-- You may also include the continuation or break condition within the directive declaration: -->
ディレクティブ宣言内に継続条件または中断条件を含めることもできます。

```blade
@foreach ($users as $user)
    @continue($user->type == 1)

    <li>{{ $user->name }}</li>

    @break($user->number == 5)
@endforeach
```

<a name="the-loop-variable"></a>
<!-- ### The Loop Variable -->
### The Loop Variable

<!-- While iterating through a `foreach` loop, a `$loop` variable will be available inside of your loop. This variable provides access to some useful bits of information such as the current loop index and whether this is the first or last iteration through the loop: -->
`foreach` ループを反復している間、ループ内で `$loop` 変数が使用可能になります。この変数は、現在のループ インデックスや、これがループの最初の反復であるか最後の反復であるかなど、いくつかの有用な情報へのアクセスを提供します。

```blade
@foreach ($users as $user)
    @if ($loop->first)
        This is the first iteration.
    @endif

    @if ($loop->last)
        This is the last iteration.
    @endif

    <p>This is user {{ $user->id }}</p>
@endforeach
```

<!-- If you are in a nested loop, you may access the parent loop's `$loop` variable via the `parent` property: -->
ネストされたループにいる場合は、`parent` プロパティを介して親ループの `$loop` 変数にアクセスできます。

```blade
@foreach ($users as $user)
    @foreach ($user->posts as $post)
        @if ($loop->parent->first)
            This is the first iteration of the parent loop.
        @endif
    @endforeach
@endforeach
```

<!-- The `$loop` variable also contains a variety of other useful properties: -->
`$loop` 変数には、他にもさまざまな便利なプロパティが含まれています。

| プロパティ           | 説明                                            |
|--------------------|--------------------------------------------------------|
| `$loop->index`     | 現在のループ反復のインデックス (0 から始まります)。 |
| `$loop->iteration` | 現在のループの繰り返し (1 から始まります)。              |
| `$loop->remaining` | ループ内に残っている反復数。                  |
| `$loop->count`     | 反復される配列内の項目の合計数。 |
| `$loop->first`     | これがループの最初の反復であるかどうか。  |
| `$loop->last`      | これがループの最後の反復であるかどうか。   |
| `$loop->even`      | これがループの均等な反復であるかどうか。    |
| `$loop->odd`       | これがループ全体での奇数の反復であるかどうか。     |
| `$loop->depth`     | 現在のループのネスト レベル。                 |
| `$loop->parent`    | ネストされたループ内の場合、親のループ変数。     |

<a name="conditional-classes"></a>
<!-- ### Conditional Classes & Styles -->
### Conditional Classes & Styles

<!-- The `@class` directive conditionally compiles a CSS class string. The directive accepts an array of classes where the array key contains the class or classes you wish to add, while the value is a boolean expression. If the array element has a numeric key, it will always be included in the rendered class list: -->
`@class` ディレクティブは、CSS クラス文字列を条件付きでコンパイルします。このディレクティブは、追加するクラスを配列キーに含み、値がブール式であるクラスの配列を受け入れます。配列要素に数値キーがある場合、その要素は常に表示されるクラス リストに含まれます。

```blade
@php
    $isActive = false;
    $hasError = true;
@endphp

<span @class([
    'p-4',
    'font-bold' => $isActive,
    'text-gray-500' => ! $isActive,
    'bg-red' => $hasError,
])></span>

<span class="p-4 text-gray-500 bg-red"></span>
```

<!-- Likewise, the `@style` directive may be used to conditionally add inline CSS styles to an HTML element: -->
同様に、`@style` ディレクティブを使用して、条件付きでインライン CSS スタイルを HTML 要素に追加できます。

```blade
@php
    $isActive = true;
@endphp

<span @style([
    'background-color: red',
    'font-weight: bold' => $isActive,
])></span>

<span style="background-color: red; font-weight: bold;"></span>
```

<a name="additional-attributes"></a>
<!-- ### Additional Attributes -->
### Additional Attributes

<!-- For convenience, you may use the `@checked` directive to easily indicate if a given HTML checkbox input is "checked". This directive will echo `checked` if the provided condition evaluates to `true`: -->
便宜上、`@checked` ディレクティブを使用して、特定の HTML チェックボックス入力が「チェックされている」かどうかを簡単に示すことができます。このディレクティブは、指定された条件が `true` と評価される場合、`checked` をエコーし​​ます。

```blade
<input type="checkbox"
        name="active"
        value="active"
        @checked(old('active', $user->active)) />
```

<!-- Likewise, the `@selected` directive may be used to indicate if a given select option should be "selected": -->
同様に、`@selected` ディレクティブを使用して、特定の選択オプションを「選択」する必要があるかどうかを示すことができます。

```blade
<select name="version">
    @foreach ($product->versions as $version)
        <option value="{{ $version }}" @selected(old('version') == $version)>
            {{ $version }}
        </option>
    @endforeach
</select>
```

<!-- Additionally, the `@disabled` directive may be used to indicate if a given element should be "disabled": -->
さらに、`@disabled` ディレクティブを使用して、特定の要素を「無効」にするかどうかを示すことができます。

```blade
<button type="submit" @disabled($errors->isNotEmpty())>Submit</button>
```

<!-- Moreover, the `@readonly` directive may be used to indicate if a given element should be "readonly": -->
さらに、`@readonly` ディレクティブを使用して、特定の要素を「読み取り専用」にするかどうかを示すことができます。

```blade
<input type="email"
        name="email"
        value="email@laravel.com"
        @readonly($user->isNotAdmin()) />
```

<!-- In addition, the `@required` directive may be used to indicate if a given element should be "required": -->
さらに、`@required` ディレクティブを使用して、特定の要素が「必須」であるかどうかを示すことができます。

```blade
<input type="text"
        name="title"
        value="title"
        @required($user->isAdmin()) />
```

<a name="including-subviews"></a>
<!-- ### Including Subviews -->
### Including Subviews

> [!NOTE]
> `@include` ディレクティブは自由に使用できますが、Blade [components](#components) は同様の機能を提供し、データや属性のバインディングなど、`@include` ディレクティブよりも優れたいくつかの利点を提供します。

<!-- Blade's `@include` directive allows you to include a Blade view from within another view. All variables that are available to the parent view will be made available to the included view: -->
Blade の `@include` ディレクティブを使用すると、別のビュー内から Blade ビューを含めることができます。親ビューで使用できるすべての変数は、組み込まれたビューでも使用できるようになります。

```blade
<div>
    @include('shared.errors')

    <form>
        <!-- Form Contents -->
    </form>
</div>
```

<!-- Even though the included view will inherit all data available in the parent view, you may also pass an array of additional data that should be made available to the included view: -->
含まれるビューは親ビューで使用可能なすべてのデータを継承しますが、含まれるビューで使用できるようにする必要がある追加データの配列を渡すこともできます。

```blade
@include('view.name', ['status' => 'complete'])
```

<!-- If you attempt to `@include` a view which does not exist, Laravel will throw an error. If you would like to include a view that may or may not be present, you should use the `@includeIf` directive: -->
存在しないビューを `@include` しようとすると、Laravel はエラーをスローします。存在するかどうかわからないビューを含めたい場合は、`@includeIf` ディレクティブを使用する必要があります。

```blade
@includeIf('view.name', ['status' => 'complete'])
```

<!-- If you would like to `@include` a view if a given boolean expression evaluates to `true` or `false`, you may use the `@includeWhen` and `@includeUnless` directives: -->
指定されたブール式が `true` または `false` に評価される場合にビューを `@include` したい場合は、`@includeWhen` および `@includeUnless` ディレクティブを使用できます。

```blade
@includeWhen($boolean, 'view.name', ['status' => 'complete'])

@includeUnless($boolean, 'view.name', ['status' => 'complete'])
```

<!-- To include the first view that exists from a given array of views, you may use the `includeFirst` directive: -->
指定されたビューの配列から存在する最初のビューを含めるには、`includeFirst` ディレクティブを使用できます。

```blade
@includeFirst(['custom.admin', 'admin'], ['status' => 'complete'])
```

> [!WARNING]
> Blade ビューでは、`__DIR__` 定数と `__FILE__` 定数を使用しないでください。これらの定数は、キャッシュされコンパイルされたビューの場所を参照するためです。

<a name="rendering-views-for-collections"></a>
<!-- #### Rendering Views for Collections -->
#### Rendering Views for Collections

<!-- You may combine loops and includes into one line with Blade's `@each` directive: -->
Blade の `@each` ディレクティブを使用して、ループとインクルードを 1 行に結合できます。

```blade
@each('view.name', $jobs, 'job')
```

<!-- The `@each` directive's first argument is the view to render for each element in the array or collection. The second argument is the array or collection you wish to iterate over, while the third argument is the variable name that will be assigned to the current iteration within the view. So, for example, if you are iterating over an array of `jobs`, typically you will want to access each job as a `job` variable within the view. The array key for the current iteration will be available as the `key` variable within the view. -->
`@each` ディレクティブの最初の引数は、配列またはコレクション内の各要素に対してレンダリングするビューです。 2 番目の引数は反復処理する配列またはコレクションで、3 番目の引数はビュー内の現在の反復に割り当てられる変数名です。したがって、たとえば、`jobs` の配列を反復処理している場合、通常はビュー内の `job` 変数として各ジョブにアクセスする必要があります。現在の反復の配列キーは、ビュー内の `key` 変数として使用できます。

<!-- You may also pass a fourth argument to the `@each` directive. This argument determines the view that will be rendered if the given array is empty. -->
`@each` ディレクティブに 4 番目の引数を渡すこともできます。この引数は、指定された配列が空の場合にレンダリングされるビューを決定します。

```blade
@each('view.name', $jobs, 'job', 'view.empty')
```

> [!WARNING]
> `@each` を介してレンダリングされたビューは、親ビューから変数を継承しません。子ビューでこれらの変数が必要な場合は、代わりに `@foreach` および `@include` ディレクティブを使用する必要があります。

<a name="the-once-directive"></a>
<!-- ### The `@once` Directive -->
### The `@once` Directive

<!-- The `@once` directive allows you to define a portion of the template that will only be evaluated once per rendering cycle. This may be useful for pushing a given piece of JavaScript into the page's header using [stacks](#stacks). For example, if you are rendering a given [component](#components) within a loop, you may wish to only push the JavaScript to the header the first time the component is rendered: -->
`@once` ディレクティブを使用すると、レンダリング サイクルごとに 1 回だけ評価されるテンプレートの部分を定義できます。これは、[stacks](#stacks) を使用して、特定の JavaScript をページのヘッダーにプッシュする場合に便利です。たとえば、ループ内で特定の [component](#components) をレンダリングする場合、コンポーネントが初めてレンダリングされるときにのみ JavaScript をヘッダーにプッシュしたい場合があります。

```blade
@once
    @push('scripts')
        <script>
            // Your custom JavaScript...
        </script>
    @endpush
@endonce
```

<!-- Since the `@once` directive is often used in conjunction with the `@push` or `@prepend` directives, the `@pushOnce` and `@prependOnce` directives are available for your convenience: -->
`@once` ディレクティブは、`@push` または `@prepend` ディレクティブと組み合わせて使用​​されることが多いため、便宜のために `@pushOnce` および `@prependOnce` ディレクティブを使用できます。

```blade
@pushOnce('scripts')
    <script>
        // Your custom JavaScript...
    </script>
@endPushOnce
```

<a name="raw-php"></a>
<!-- ### Raw PHP -->
### Raw PHP

<!-- In some situations, it's useful to embed PHP code into your views. You can use the Blade `@php` directive to execute a block of plain PHP within your template: -->
状況によっては、PHP コードをビューに埋め込むと便利です。 Blade `@php` ディレクティブを使用して、テンプレート内のプレーン PHP のブロックを実行できます。

```blade
@php
    $counter = 1;
@endphp
```

<!-- Or, if you only need to use PHP to import a class, you may use the `@use` directive: -->
または、クラスのインポートに PHP のみを使用する必要がある場合は、`@use` ディレクティブを使用できます。

```blade
@use('App\Models\Flight')
```

<!-- A second argument may be provided to the `@use` directive to alias the imported class: -->
2 番目の引数を `@use` ディレクティブに指定して、インポートされたクラスの別名を付けることができます。

```php
@use('App\Models\Flight', 'FlightModel')
```

<a name="comments"></a>
<!-- ### Comments -->
### Comments

<!-- Blade also allows you to define comments in your views. However, unlike HTML comments, Blade comments are not included in the HTML returned by your application: -->
Blade では、ビュー内にコメントを定義することもできます。ただし、HTML コメントとは異なり、Blade コメントはアプリケーションから返される HTML には含まれません。

```blade
{{-- This comment will not be present in the rendered HTML --}}
```

<a name="components"></a>
<!-- ## Components -->
## Components

<!-- Components and slots provide similar benefits to sections, layouts, and includes; however, some may find the mental model of components and slots easier to understand. There are two approaches to writing components: class based components and anonymous components. -->
コンポーネントとスロットは、セクション、レイアウト、インクルードに同様の利点をもたらします。ただし、コンポーネントとスロットのメンタル モデルの方が理解しやすいと感じる人もいるかもしれません。コンポーネントを作成するには、クラスベースのコンポーネントと匿名コンポーネントの 2 つのアプローチがあります。

<!-- To create a class based component, you may use the `make:component` Artisan command. To illustrate how to use components, we will create a simple `Alert` component. The `make:component` command will place the component in the `app/View/Components` directory: -->
クラスベースのコンポーネントを作成するには、`make:component` Artisan コマンドを使用できます。コンポーネントの使用方法を説明するために、単純な `Alert` コンポーネントを作成します。 `make:component` コマンドは、コンポーネントを `app/View/Components` ディレクトリに配置します。

```shell
php artisan make:component Alert
```

<!-- The `make:component` command will also create a view template for the component. The view will be placed in the `resources/views/components` directory. When writing components for your own application, components are automatically discovered within the `app/View/Components` directory and `resources/views/components` directory, so no further component registration is typically required. -->
`make:component` コマンドは、コンポーネントのビュー テンプレートも作成します。ビューは `resources/views/components` ディレクトリに配置されます。独自のアプリケーションのコンポーネントを作成する場合、コンポーネントは `app/View/Components` ディレクトリおよび `resources/views/components` ディレクトリ内で自動的に検出されるため、通常は追加のコンポーネントの登録は必要ありません。

<!-- You may also create components within subdirectories: -->
サブディレクトリ内にコンポーネントを作成することもできます。

```shell
php artisan make:component Forms/Input
```

<!-- The command above will create an `Input` component in the `app/View/Components/Forms` directory and the view will be placed in the `resources/views/components/forms` directory. -->
上記のコマンドは、`app/View/Components/Forms` ディレクトリに `Input` コンポーネントを作成し、ビューは `resources/views/components/forms` ディレクトリに配置されます。

<!-- If you would like to create an anonymous component (a component with only a Blade template and no class), you may use the `--view` flag when invoking the `make:component` command: -->
匿名コンポーネント (Blade テンプレートのみでクラスを持たないコンポーネント) を作成する場合は、`make:component` コマンドを呼び出すときに `--view` フラグを使用できます。

```shell
php artisan make:component forms.input --view
```

<!-- The command above will create a Blade file at `resources/views/components/forms/input.blade.php` which can be rendered as a component via `<x-forms.input />`. -->
上記のコマンドは、`resources/views/components/forms/input.blade.php` に Blade ファイルを作成し、`<x-forms.input />` を介してコンポーネントとしてレンダリングできます。

<a name="manually-registering-package-components"></a>
<!-- #### Manually Registering Package Components -->
#### Manually Registering Package Components

<!-- When writing components for your own application, components are automatically discovered within the `app/View/Components` directory and `resources/views/components` directory. -->
独自のアプリケーションのコンポーネントを作成する場合、コンポーネントは `app/View/Components` ディレクトリおよび `resources/views/components` ディレクトリ内で自動的に検出されます。

<!-- However, if you are building a package that utilizes Blade components, you will need to manually register your component class and its HTML tag alias. You should typically register your components in the `boot` method of your package's service provider: -->
ただし、Blade コンポーネントを利用するパッケージを構築している場合は、コンポーネント クラスとその HTML タグ エイリアスを手動で登録する必要があります。通常、コンポーネントはパッケージのサービスプロバイダの `boot` メソッドに登録する必要があります。

```
use Illuminate\Support\Facades\Blade;

/**
 * Bootstrap your package's services.
 */
public function boot(): void
{
    Blade::component('package-alert', Alert::class);
}
```

<!-- Once your component has been registered, it may be rendered using its tag alias: -->
コンポーネントが登録されると、そのタグ エイリアスを使用してレンダリングできます。

```blade
<x-package-alert/>
```

<!-- Alternatively, you may use the `componentNamespace` method to autoload component classes by convention. For example, a `Nightshade` package might have `Calendar` and `ColorPicker` components that reside within the `Package\Views\Components` namespace: -->
あるいは、`componentNamespace` メソッドを使用して、規則に従ってコンポーネント クラスを自動ロードすることもできます。たとえば、`Nightshade` パッケージには、`Package\Views\Components` 名前空間内に存在する `Calendar` コンポーネントと `ColorPicker` コンポーネントが含まれる場合があります。

```
use Illuminate\Support\Facades\Blade;

/**
 * Bootstrap your package's services.
 */
public function boot(): void
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```

<!-- This will allow the usage of package components by their vendor namespace using the `package-name::` syntax: -->
これにより、`package-name::` 構文を使用して、ベンダー名前空間によるパッケージ コンポーネントの使用が許可されます。

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

<!-- Blade will automatically detect the class that's linked to this component by pascal-casing the component name. Subdirectories are also supported using "dot" notation. -->
Blade は、コンポーネント名をパスカル文字に変換することで、このコンポーネントにリンクされているクラスを自動的に検出します。サブディレクトリは、「ドット」表記を使用してサポートされています。

<a name="rendering-components"></a>
<!-- ### Rendering Components -->
### Rendering Components

<!-- To display a component, you may use a Blade component tag within one of your Blade templates. Blade component tags start with the string `x-` followed by the kebab case name of the component class: -->
コンポーネントを表示するには、Blade テンプレートの 1 つ内で Blade コンポーネント タグを使用できます。Blade コンポーネント タグは文字列 `x-` で始まり、その後にコンポーネント クラスのケバブ ケース名が続きます。

```blade
<x-alert/>

<x-user-profile/>
```

<!-- If the component class is nested deeper within the `app/View/Components` directory, you may use the `.` character to indicate directory nesting. For example, if we assume a component is located at `app/View/Components/Inputs/Button.php`, we may render it like so: -->
コンポーネント クラスが `app/View/Components` ディレクトリ内でさらに深くネストされている場合は、ディレクトリのネストを示すために `.` 文字を使用できます。たとえば、コンポーネントが `app/View/Components/Inputs/Button.php` にあると仮定すると、次のようにレンダリングできます。

```blade
<x-inputs.button/>
```

<!-- If you would like to conditionally render your component, you may define a `shouldRender` method on your component class. If the `shouldRender` method returns `false` the component will not be rendered: -->
コンポーネントを条件付きでレンダリングしたい場合は、コンポーネント クラスで `shouldRender` メソッドを定義できます。 `shouldRender` メソッドが `false` を返す場合、コンポーネントはレンダリングされません。

```
use Illuminate\Support\Str;

/**
 * Whether the component should be rendered
 */
public function shouldRender(): bool
{
    return Str::length($this->message) > 0;
}
```

<a name="passing-data-to-components"></a>
<!-- ### Passing Data to Components -->
### Passing Data to Components

<!-- You may pass data to Blade components using HTML attributes. Hard-coded, primitive values may be passed to the component using simple HTML attribute strings. PHP expressions and variables should be passed to the component via attributes that use the `:` character as a prefix: -->
HTML 属性を使用してデータを Blade コンポーネントに渡すことができます。ハードコーディングされたプリミティブ値は、単純な HTML 属性文字列を使用してコンポーネントに渡すことができます。 PHP 式と変数は、接頭辞として `:` 文字を使用する属性を介してコンポーネントに渡す必要があります。

```blade
<x-alert type="error" :message="$message"/>
```

<!-- You should define all of the component's data attributes in its class constructor. All public properties on a component will automatically be made available to the component's view. It is not necessary to pass the data to the view from the component's `render` method: -->
コンポーネントのすべてのデータ属性をそのクラス コンストラクターで定義する必要があります。コンポーネント上のすべてのパブリック プロパティは、コンポーネントのビューで自動的に利用できるようになります。コンポーネントの `render` メソッドからビューにデータを渡す必要はありません。

```
<?php

namespace App\View\Components;

use Illuminate\View\Component;
use Illuminate\View\View;

class Alert extends Component
{
    /**
     * Create the component instance.
     */
    public function __construct(
        public string $type,
        public string $message,
    ) {}

    /**
     * Get the view / contents that represent the component.
     */
    public function render(): View
    {
        return view('components.alert');
    }
}
```

<!-- When your component is rendered, you may display the contents of your component's public variables by echoing the variables by name: -->
コンポーネントがレンダリングされるとき、変数を名前でエコーすることによって、コンポーネントのパブリック変数の内容を表示できます。

```blade
<div class="alert alert-{{ $type }}">
    {{ $message }}
</div>
```

<a name="casing"></a>
<!-- #### Casing -->
#### Casing

<!-- Component constructor arguments should be specified using `camelCase`, while `kebab-case` should be used when referencing the argument names in your HTML attributes. For example, given the following component constructor: -->
コンポーネントのコンストラクター引数は `camelCase` を使用して指定する必要がありますが、HTML 属性の引数名を参照する場合は `kebab-case` を使用する必要があります。たとえば、次のコンポーネント コンストラクターがあるとします。

```
/**
 * Create the component instance.
 */
public function __construct(
    public string $alertType,
) {}
```

<!-- The `$alertType` argument may be provided to the component like so: -->
`$alertType` 引数は、次のようにコンポーネントに指定できます。

```blade
<x-alert alert-type="danger" />
```

<a name="short-attribute-syntax"></a>
<!-- #### Short Attribute Syntax -->
#### Short Attribute Syntax

<!-- When passing attributes to components, you may also use a "short attribute" syntax. This is often convenient since attribute names frequently match the variable names they correspond to: -->
コンポーネントに属性を渡すときは、「短い属性」構文を使用することもできます。属性名は、対応する変数名と一致することが多いため、これは便利なことがよくあります。

```blade
{{-- Short attribute syntax... --}}
<x-profile :$userId :$name />

{{-- Is equivalent to... --}}
<x-profile :user-id="$userId" :name="$name" />
```

<a name="escaping-attribute-rendering"></a>
<!-- #### Escaping Attribute Rendering -->
#### Escaping Attribute Rendering

<!-- Since some JavaScript frameworks such as Alpine.js also use colon-prefixed attributes, you may use a double colon (`::`) prefix to inform Blade that the attribute is not a PHP expression. For example, given the following component: -->
Alpine.js などの一部の JavaScript フレームワークもコロン接頭辞付きの属性を使用するため、二重コロン (`::`) 接頭辞を使用して属性が PHP 式ではないことを Blade に通知できます。たとえば、次のコンポーネントがあるとします。

```blade
<x-button ::class="{ danger: isDeleting }">
    Submit
</x-button>
```

<!-- The following HTML will be rendered by Blade: -->
次の HTML が Blade によってレンダリングされます。

```blade
<button :class="{ danger: isDeleting }">
    Submit
</button>
```

<a name="component-methods"></a>
<!-- #### Component Methods -->
#### Component Methods

<!-- In addition to public variables being available to your component template, any public methods on the component may be invoked. For example, imagine a component that has an `isSelected` method: -->
コンポーネント テンプレートで使用できるパブリック変数に加えて、コンポーネント上の任意のパブリック メソッドを呼び出すことができます。たとえば、`isSelected` メソッドを持つコンポーネントを想像してください。

```
/**
 * Determine if the given option is the currently selected option.
 */
public function isSelected(string $option): bool
{
    return $option === $this->selected;
}
```

<!-- You may execute this method from your component template by invoking the variable matching the name of the method: -->
メソッドの名前に一致する変数を呼び出すことで、コンポーネント テンプレートからこのメソッドを実行できます。

```blade
<option {{ $isSelected($value) ? 'selected' : '' }} value="{{ $value }}">
    {{ $label }}
</option>
```

<a name="using-attributes-slots-within-component-class"></a>
<!-- #### Accessing Attributes and Slots Within Component Classes -->
#### Accessing Attributes and Slots Within Component Classes

<!-- Blade components also allow you to access the component name, attributes, and slot inside the class's render method. However, in order to access this data, you should return a closure from your component's `render` method. The closure will receive a `$data` array as its only argument. This array will contain several elements that provide information about the component: -->
Blade コンポーネントを使用すると、クラスの render メソッド内のコンポーネント名、属性、スロットにアクセスすることもできます。ただし、このデータにアクセスするには、コンポーネントの `render` メソッドからクロージャを返す必要があります。クロージャは、唯一の引数として `$data` 配列を受け取ります。この配列には、コンポーネントに関する情報を提供するいくつかの要素が含まれます。

```
use Closure;

/**
 * Get the view / contents that represent the component.
 */
public function render(): Closure
{
    return function (array $data) {
        // $data['componentName'];
        // $data['attributes'];
        // $data['slot'];

        return '<div>Components content</div>';
    };
}
```

<!-- The `componentName` is equal to the name used in the HTML tag after the `x-` prefix. So `<x-alert />`'s `componentName` will be `alert`. The `attributes` element will contain all of the attributes that were present on the HTML tag. The `slot` element is an `Illuminate\Support\HtmlString` instance with the contents of the component's slot. -->
`componentName` は、HTML タグで `x-` プレフィックスの後に使用される名前と同じです。したがって、`<x-alert />` の `componentName` は `alert` になります。 `attributes` 要素には、HTML タグに存在したすべての属性が含まれます。 `slot` 要素は、コンポーネントのスロットの内容を含む `Illuminate\Support\HtmlString` インスタンスです。

<!-- The closure should return a string. If the returned string corresponds to an existing view, that view will be rendered; otherwise, the returned string will be evaluated as an inline Blade view. -->
クロージャは文字列を返す必要があります。返された文字列が既存のビューに対応する場合、そのビューがレンダリングされます。それ以外の場合、返された文字列はインライン Blade ビューとして評価されます。

<a name="additional-dependencies"></a>
<!-- #### Additional Dependencies -->
#### Additional Dependencies

<!-- If your component requires dependencies from Laravel's [service container](/docs/10.x/container), you may list them before any of the component's data attributes and they will automatically be injected by the container: -->
コンポーネントが Laravel の [service container](/docs/10.x/container) からの依存関係を必要とする場合、コンポーネントのデータ属性の前に依存関係をリストすると、それらはコンテナーによって自動的に挿入されます。

```php
use App\Services\AlertCreator;

/**
 * Create the component instance.
 */
public function __construct(
    public AlertCreator $creator,
    public string $type,
    public string $message,
) {}
```

<a name="hiding-attributes-and-methods"></a>
<!-- #### Hiding Attributes / Methods -->
#### Hiding Attributes / Methods

<!-- If you would like to prevent some public methods or properties from being exposed as variables to your component template, you may add them to an `$except` array property on your component: -->
一部のパブリック メソッドまたはプロパティが変数としてコンポーネント テンプレートに公開されるのを防ぎたい場合は、それらをコンポーネントの `$except` 配列プロパティに追加できます。

```
<?php

namespace App\View\Components;

use Illuminate\View\Component;

class Alert extends Component
{
    /**
     * The properties / methods that should not be exposed to the component template.
     *
     * @var array
     */
    protected $except = ['type'];

    /**
     * Create the component instance.
     */
    public function __construct(
        public string $type,
    ) {}
}
```

<a name="component-attributes"></a>
<!-- ### Component Attributes -->
### Component Attributes

<!-- We've already examined how to pass data attributes to a component; however, sometimes you may need to specify additional HTML attributes, such as `class`, that are not part of the data required for a component to function. Typically, you want to pass these additional attributes down to the root element of the component template. For example, imagine we want to render an `alert` component like so: -->
データ属性をコンポーネントに渡す方法はすでに検討しました。ただし、コンポーネントが機能するために必要なデータの一部ではない、`class` などの追加の HTML 属性を指定する必要がある場合があります。通常、これらの追加属性はコンポーネント テンプレートのルート要素に渡します。たとえば、次のように `alert` コンポーネントをレンダリングしたいとします。

```blade
<x-alert type="error" :message="$message" class="mt-4"/>
```

<!-- All of the attributes that are not part of the component's constructor will automatically be added to the component's "attribute bag". This attribute bag is automatically made available to the component via the `$attributes` variable. All of the attributes may be rendered within the component by echoing this variable: -->
コンポーネントのコンストラクターの一部ではないすべての属性は、コンポーネントの「属性バッグ」に自動的に追加されます。この属性バッグは、`$attributes` 変数を介してコンポーネントで自動的に使用できるようになります。この変数をエコーすることで、すべての属性をコンポーネント内でレンダリングできます。

```blade
<div {{ $attributes }}>
    <!-- Component content -->
</div>
```

> [!WARNING]
> 現時点では、コンポーネント タグ内での `@env` などのディレクティブの使用はサポートされていません。たとえば、`<x-alert :live="@env('production')"/>` はコンパイルされません。

<a name="default-merged-attributes"></a>
<!-- #### Default / Merged Attributes -->
#### Default / Merged Attributes

<!-- Sometimes you may need to specify default values for attributes or merge additional values into some of the component's attributes. To accomplish this, you may use the attribute bag's `merge` method. This method is particularly useful for defining a set of default CSS classes that should always be applied to a component: -->
場合によっては、属性のデフォルト値を指定したり、コンポーネントの属性の一部に追加の値をマージしたりすることが必要な場合があります。これを実現するには、属性バッグの `merge` メソッドを使用できます。このメソッドは、コンポーネントに常に適用する必要がある一連のデフォルト CSS クラスを定義する場合に特に役立ちます。

```blade
<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

<!-- If we assume this component is utilized like so: -->
このコンポーネントが次のように利用されると仮定すると、次のようになります。

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

<!-- The final, rendered HTML of the component will appear like the following: -->
コンポーネントの最終的にレンダリングされた HTML は次のように表示されます。

```blade
<div class="alert alert-error mb-4">
    <!-- Contents of the $message variable -->
</div>
```

<a name="conditionally-merge-classes"></a>
<!-- #### Conditionally Merge Classes -->
#### Conditionally Merge Classes

<!-- Sometimes you may wish to merge classes if a given condition is `true`. You can accomplish this via the `class` method, which accepts an array of classes where the array key contains the class or classes you wish to add, while the value is a boolean expression. If the array element has a numeric key, it will always be included in the rendered class list: -->
特定の条件が `true` の場合、クラスをマージしたい場合があります。これは、`class` メソッドを使用して実行できます。このメソッドは、値がブール式の場合、配列キーに追加するクラスが含まれるクラスの配列を受け取ります。配列要素に数値キーがある場合、その要素は常に表示されるクラス リストに含まれます。

```blade
<div {{ $attributes->class(['p-4', 'bg-red' => $hasError]) }}>
    {{ $message }}
</div>
```

<!-- If you need to merge other attributes onto your component, you can chain the `merge` method onto the `class` method: -->
他の属性をコンポーネントにマージする必要がある場合は、`merge` メソッドを `class` メソッドにチェーンできます。

```blade
<button {{ $attributes->class(['p-4'])->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

> [!NOTE]
> マージされた属性を受け取るべきではない他の HTML 要素のクラスを条件付きでコンパイルする必要がある場合は、[`@class` directive](#conditional-classes) を使用できます。

<a name="non-class-attribute-merging"></a>
<!-- #### Non-Class Attribute Merging -->
#### Non-Class Attribute Merging

<!-- When merging attributes that are not `class` attributes, the values provided to the `merge` method will be considered the "default" values of the attribute. However, unlike the `class` attribute, these attributes will not be merged with injected attribute values. Instead, they will be overwritten. For example, a `button` component's implementation may look like the following: -->
`class` 属性ではない属性をマージする場合、`merge` メソッドに指定された値は属性の「デフォルト」値とみなされます。ただし、`class` 属性とは異なり、これらの属性は挿入された属性値とマージされません。代わりに、上書きされます。たとえば、`button` コンポーネントの実装は次のようになります。

```blade
<button {{ $attributes->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

<!-- To render the button component with a custom `type`, it may be specified when consuming the component. If no type is specified, the `button` type will be used: -->
カスタム `type` を使用してボタン コンポーネントをレンダリングするには、コンポーネントを使用するときに指定できます。タイプが指定されていない場合は、`button` タイプが使用されます。

```blade
<x-button type="submit">
    Submit
</x-button>
```

<!-- The rendered HTML of the `button` component in this example would be: -->
この例の `button` コンポーネントのレンダリングされた HTML は次のようになります。

```blade
<button type="submit">
    Submit
</button>
```

<!-- If you would like an attribute other than `class` to have its default value and injected values joined together, you may use the `prepends` method. In this example, the `data-controller` attribute will always begin with `profile-controller` and any additional injected `data-controller` values will be placed after this default value: -->
`class` 以外の属性のデフォルト値と挿入された値を結合したい場合は、`prepends` メソッドを使用できます。この例では、`data-controller` 属性は常に `profile-controller` で始まり、追加で挿入された `data-controller` 値はこのデフォルト値の後に配置されます。

```blade
<div {{ $attributes->merge(['data-controller' => $attributes->prepends('profile-controller')]) }}>
    {{ $slot }}
</div>
```

<a name="filtering-attributes"></a>
<!-- #### Retrieving and Filtering Attributes -->
#### Retrieving and Filtering Attributes

<!-- You may filter attributes using the `filter` method. This method accepts a closure which should return `true` if you wish to retain the attribute in the attribute bag: -->
`filter` メソッドを使用して属性をフィルタリングできます。このメソッドは、属性バッグに属性を保持したい場合に `true` を返すクロージャを受け入れます。

```blade
{{ $attributes->filter(fn (string $value, string $key) => $key == 'foo') }}
```

<!-- For convenience, you may use the `whereStartsWith` method to retrieve all attributes whose keys begin with a given string: -->
便宜上、`whereStartsWith` メソッドを使用して、キーが指定された文字列で始まるすべての属性を取得できます。

```blade
{{ $attributes->whereStartsWith('wire:model') }}
```

<!-- Conversely, the `whereDoesntStartWith` method may be used to exclude all attributes whose keys begin with a given string: -->
逆に、`whereDoesntStartWith` メソッドを使用して、キーが指定された文字列で始まるすべての属性を除外することもできます。

```blade
{{ $attributes->whereDoesntStartWith('wire:model') }}
```

<!-- Using the `first` method, you may render the first attribute in a given attribute bag: -->
`first` メソッドを使用すると、指定された属性バッグの最初の属性をレンダリングできます。

```blade
{{ $attributes->whereStartsWith('wire:model')->first() }}
```

<!-- If you would like to check if an attribute is present on the component, you may use the `has` method. This method accepts the attribute name as its only argument and returns a boolean indicating whether or not the attribute is present: -->
コンポーネントに属性が存在するかどうかを確認したい場合は、`has` メソッドを使用できます。このメソッドは、属性名を唯一の引数として受け入れ、属性が存在するかどうかを示すブール値を返します。

```blade
@if ($attributes->has('class'))
    <div>Class attribute is present</div>
@endif
```

<!-- If an array is passed to the `has` method, the method will determine if all of the given attributes are present on the component: -->
配列が `has` メソッドに渡される場合、メソッドは指定された属性がすべてコンポーネントに存在するかどうかを判断します。

```blade
@if ($attributes->has(['name', 'class']))
    <div>All of the attributes are present</div>
@endif
```

<!-- The `hasAny` method may be used to determine if any of the given attributes are present on the component: -->
`hasAny` メソッドは、指定された属性のいずれかがコンポーネントに存在するかどうかを判断するために使用できます。

```blade
@if ($attributes->hasAny(['href', ':href', 'v-bind:href']))
    <div>One of the attributes is present</div>
@endif
```

<!-- You may retrieve a specific attribute's value using the `get` method: -->
`get` メソッドを使用して、特定の属性の値を取得できます。

```blade
{{ $attributes->get('class') }}
```

<a name="reserved-keywords"></a>
<!-- ### Reserved Keywords -->
### Reserved Keywords

<!-- By default, some keywords are reserved for Blade's internal use in order to render components. The following keywords cannot be defined as public properties or method names within your components: -->
デフォルトでは、一部のキーワードはコンポーネントをレンダリングするために Blade の内部使用のために予約されています。次のキーワードは、コンポーネント内のパブリック プロパティまたはメソッド名として定義できません。

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `data`
- `render`
- `resolveView`
- `shouldRender`
- `view`
- `withAttributes`
- `withName`
-->
- `data`
- `render`
- `resolveView`
- `shouldRender`
- `view`
- `withAttributes`
- `withName`

<!-- </div> -->
</div>

<a name="slots"></a>
<!-- ### Slots -->
### Slots

<!-- You will often need to pass additional content to your component via "slots". Component slots are rendered by echoing the `$slot` variable. To explore this concept, let's imagine that an `alert` component has the following markup: -->
多くの場合、追加のコンテンツを「スロット」経由でコンポーネントに渡す必要があります。コンポーネント スロットは、`$slot` 変数をエコーすることによってレンダリングされます。この概念を詳しく調べるために、`alert` コンポーネントに次のマークアップがあると想像してみましょう。

```blade
<!-- /resources/views/components/alert.blade.php -->

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

<!-- We may pass content to the `slot` by injecting content into the component: -->
コンポーネントにコンテンツを挿入することで、コンテンツを `slot` に渡すことができます。

```blade
<x-alert>
    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

<!-- Sometimes a component may need to render multiple different slots in different locations within the component. Let's modify our alert component to allow for the injection of a "title" slot: -->
場合によっては、コンポーネントがコンポーネント内の異なる場所に複数の異なるスロットをレンダリングする必要がある場合があります。 「タイトル」スロットを挿入できるようにアラート コンポーネントを変更しましょう。

```blade
<!-- /resources/views/components/alert.blade.php -->

<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

<!-- You may define the content of the named slot using the `x-slot` tag. Any content not within an explicit `x-slot` tag will be passed to the component in the `$slot` variable: -->
`x-slot` タグを使用して、名前付きスロットの内容を定義できます。明示的な `x-slot` タグ内にないコンテンツは、`$slot` 変数のコンポーネントに渡されます。

```xml
<x-alert>
    <x-slot:title>
        Server Error
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

<!-- You may invoke a slot's `isEmpty` method to determine if the slot contains content: -->
スロットの `isEmpty` メソッドを呼び出して、スロットにコンテンツが含まれているかどうかを確認できます。

```blade
<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    @if ($slot->isEmpty())
        This is default content if the slot is empty.
    @else
        {{ $slot }}
    @endif
</div>
```

<!-- Additionally, the `hasActualContent` method may be used to determine if the slot contains any "actual" content that is not an HTML comment: -->
さらに、`hasActualContent` メソッドを使用して、スロットに HTML コメントではない「実際の」コンテンツが含まれているかどうかを判断できます。

```blade
@if ($slot->hasActualContent())
    The scope has non-comment content.
@endif
```

<a name="scoped-slots"></a>
<!-- #### Scoped Slots -->
#### Scoped Slots

<!-- If you have used a JavaScript framework such as Vue, you may be familiar with "scoped slots", which allow you to access data or methods from the component within your slot. You may achieve similar behavior in Laravel by defining public methods or properties on your component and accessing the component within your slot via the `$component` variable. In this example, we will assume that the `x-alert` component has a public `formatAlert` method defined on its component class: -->
Vue などの JavaScript フレームワークを使用したことがある場合は、スロット内のコンポーネントからデータまたはメソッドにアクセスできる「スコープ スロット」に精通しているかもしれません。コンポーネント上でパブリックメソッドまたはプロパティを定義し、`$component` 変数を介してスロット内のコンポーネントにアクセスすることで、Laravel でも同様の動作を実現できます。この例では、`x-alert` コンポーネントのコンポーネント クラスにパブリック `formatAlert` メソッドが定義されていると仮定します。

```blade
<x-alert>
    <x-slot:title>
        {{ $component->formatAlert('Server Error') }}
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

<a name="slot-attributes"></a>
<!-- #### Slot Attributes -->
#### Slot Attributes

<!-- Like Blade components, you may assign additional [attributes](#component-attributes) to slots such as CSS class names: -->
Blade コンポーネントと同様に、CSS クラス名などのスロットに追加の [attributes](#component-attributes) を割り当てることができます。

```xml
<x-card class="shadow-sm">
    <x-slot:heading class="font-bold">
        Heading
    </x-slot>

    Content

    <x-slot:footer class="text-sm">
        Footer
    </x-slot>
</x-card>
```

<!-- To interact with slot attributes, you may access the `attributes` property of the slot's variable. For more information on how to interact with attributes, please consult the documentation on [component attributes](#component-attributes): -->
スロット属性を操作するには、スロットの変数の `attributes` プロパティにアクセスします。属性の操作方法の詳細については、[component attributes](#component-attributes) のドキュメントを参照してください。

```blade
@props([
    'heading',
    'footer',
])

<div {{ $attributes->class(['border']) }}>
    <h1 {{ $heading->attributes->class(['text-lg']) }}>
        {{ $heading }}
    </h1>

    {{ $slot }}

    <footer {{ $footer->attributes->class(['text-gray-700']) }}>
        {{ $footer }}
    </footer>
</div>
```

<a name="inline-component-views"></a>
<!-- ### Inline Component Views -->
### Inline Component Views

<!-- For very small components, it may feel cumbersome to manage both the component class and the component's view template. For this reason, you may return the component's markup directly from the `render` method: -->
非常に小さなコンポーネントの場合、コンポーネント クラスとコンポーネントのビュー テンプレートの両方を管理するのが面倒に感じる場合があります。このため、コンポーネントのマークアップを `render` メソッドから直接返すことができます。

```
/**
 * Get the view / contents that represent the component.
 */
public function render(): string
{
    return <<<'blade'
        <div class="alert alert-danger">
            {{ $slot }}
        </div>
    blade;
}
```

<a name="generating-inline-view-components"></a>
<!-- #### Generating Inline View Components -->
#### Generating Inline View Components

<!-- To create a component that renders an inline view, you may use the `inline` option when executing the `make:component` command: -->
インライン ビューをレンダリングするコンポーネントを作成するには、`make:component` コマンドの実行時に `inline` オプションを使用できます。

```shell
php artisan make:component Alert --inline
```

<a name="dynamic-components"></a>
<!-- ### Dynamic Components -->
### Dynamic Components

<!-- Sometimes you may need to render a component but not know which component should be rendered until runtime. In this situation, you may use Laravel's built-in `dynamic-component` component to render the component based on a runtime value or variable: -->
コンポーネントをレンダリングする必要があるが、実行時までどのコンポーネントをレンダリングすべきかわからない場合があります。この状況では、Laravel の組み込み `dynamic-component` コンポーネントを使用して、実行時の値または変数に基づいてコンポーネントをレンダリングできます。

```blade
// $componentName = "secondary-button";

<x-dynamic-component :component="$componentName" class="mt-4" />
```

<a name="manually-registering-components"></a>
<!-- ### Manually Registering Components -->
### Manually Registering Components

> [!WARNING]
> コンポーネントの手動登録に関する次のドキュメントは、主にビューコンポーネントを含む Laravel パッケージを作成する人に適用されます。パッケージを作成していない場合、コンポーネントのドキュメントのこの部分は関係ない可能性があります。

<!-- When writing components for your own application, components are automatically discovered within the `app/View/Components` directory and `resources/views/components` directory. -->
独自のアプリケーションのコンポーネントを作成する場合、コンポーネントは `app/View/Components` ディレクトリおよび `resources/views/components` ディレクトリ内で自動的に検出されます。

<!-- However, if you are building a package that utilizes Blade components or placing components in non-conventional directories, you will need to manually register your component class and its HTML tag alias so that Laravel knows where to find the component. You should typically register your components in the `boot` method of your package's service provider: -->
ただし、Blade コンポーネントを利用するパッケージを構築する場合、またはコンポーネントを従来とは異なるディレクトリに配置する場合は、Laravel がコンポーネントの場所を認識できるように、コンポーネント クラスとその HTML タグのエイリアスを手動で登録する必要があります。通常、コンポーネントはパッケージのサービスプロバイダの `boot` メソッドに登録する必要があります。

```
use Illuminate\Support\Facades\Blade;
use VendorPackage\View\Components\AlertComponent;

/**
 * Bootstrap your package's services.
 */
public function boot(): void
{
    Blade::component('package-alert', AlertComponent::class);
}
```

<!-- Once your component has been registered, it may be rendered using its tag alias: -->
コンポーネントが登録されると、そのタグ エイリアスを使用してレンダリングできます。

```blade
<x-package-alert/>
```

<!-- #### Autoloading Package Components -->
#### Autoloading Package Components

<!-- Alternatively, you may use the `componentNamespace` method to autoload component classes by convention. For example, a `Nightshade` package might have `Calendar` and `ColorPicker` components that reside within the `Package\Views\Components` namespace: -->
あるいは、`componentNamespace` メソッドを使用して、規則に従ってコンポーネント クラスを自動ロードすることもできます。たとえば、`Nightshade` パッケージには、`Package\Views\Components` 名前空間内に存在する `Calendar` コンポーネントと `ColorPicker` コンポーネントが含まれる場合があります。

```
use Illuminate\Support\Facades\Blade;

/**
 * Bootstrap your package's services.
 */
public function boot(): void
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```

<!-- This will allow the usage of package components by their vendor namespace using the `package-name::` syntax: -->
これにより、`package-name::` 構文を使用して、ベンダー名前空間によるパッケージ コンポーネントの使用が許可されます。

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

<!-- Blade will automatically detect the class that's linked to this component by pascal-casing the component name. Subdirectories are also supported using "dot" notation. -->
Blade は、コンポーネント名をパスカル文字に変換することで、このコンポーネントにリンクされているクラスを自動的に検出します。サブディレクトリは、「ドット」表記を使用してサポートされています。

<a name="anonymous-components"></a>
<!-- ## Anonymous Components -->
## Anonymous Components

<!-- Similar to inline components, anonymous components provide a mechanism for managing a component via a single file. However, anonymous components utilize a single view file and have no associated class. To define an anonymous component, you only need to place a Blade template within your `resources/views/components` directory. For example, assuming you have defined a component at `resources/views/components/alert.blade.php`, you may simply render it like so: -->
インライン コンポーネントと同様に、匿名コンポーネントは、単一のファイルを介してコンポーネントを管理するメカニズムを提供します。ただし、匿名コンポーネントは単一のビュー ファイルを使用し、関連するクラスを持ちません。匿名コンポーネントを定義するには、`resources/views/components` ディレクトリ内に Blade テンプレートを配置するだけです。たとえば、`resources/views/components/alert.blade.php` でコンポーネントを定義したと仮定すると、次のように単純にレンダリングできます。

```blade
<x-alert/>
```

<!-- You may use the `.` character to indicate if a component is nested deeper inside the `components` directory. For example, assuming the component is defined at `resources/views/components/inputs/button.blade.php`, you may render it like so: -->
`.` 文字を使用して、コンポーネントが `components` ディレクトリのさらに深くネストされているかどうかを示すことができます。たとえば、コンポーネントが `resources/views/components/inputs/button.blade.php` で定義されていると仮定すると、次のようにレンダリングできます。

```blade
<x-inputs.button/>
```

<a name="anonymous-index-components"></a>
<!-- ### Anonymous Index Components -->
### Anonymous Index Components

<!-- Sometimes, when a component is made up of many Blade templates, you may wish to group the given component's templates within a single directory. For example, imagine an "accordion" component with the following directory structure: -->
コンポーネントが多数の Blade テンプレートで構成されている場合、特定のコンポーネントのテンプレートを 1 つのディレクトリ内にグループ化したい場合があります。たとえば、次のディレクトリ構造を持つ「accordion」コンポーネントを想像してください。

```none
/resources/views/components/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

<!-- This directory structure allows you to render the accordion component and its item like so: -->
このディレクトリ構造により、アコーディオン コンポーネントとその項目を次のようにレンダリングできます。

```blade
<x-accordion>
    <x-accordion.item>
        ...
    </x-accordion.item>
</x-accordion>
```

<!-- However, in order to render the accordion component via `x-accordion`, we were forced to place the "index" accordion component template in the `resources/views/components` directory instead of nesting it within the `accordion` directory with the other accordion related templates. -->
ただし、`x-accordion` 経由でアコーディオン コンポーネントをレンダリングするには、「インデックス」アコーディオン コンポーネント テンプレートを、他のアコーディオン関連テンプレートとともに `accordion` ディレクトリ内にネストするのではなく、`resources/views/components` ディレクトリに配置する必要がありました。

<!-- Thankfully, Blade allows you to place an `index.blade.php` file within a component's template directory. When an `index.blade.php` template exists for the component, it will be rendered as the "root" node of the component. So, we can continue to use the same Blade syntax given in the example above; however, we will adjust our directory structure like so: -->
ありがたいことに、Blade では、コンポーネントのテンプレート ディレクトリ内に `index.blade.php` ファイルを配置できます。コンポーネントに `index.blade.php` テンプレートが存在する場合、それはコンポーネントの「ルート」ノードとしてレンダリングされます。したがって、上記の例で示した同じ Blade 構文を引き続き使用できます。ただし、ディレクトリ構造は次のように調整します。

```none
/resources/views/components/accordion/index.blade.php
/resources/views/components/accordion/item.blade.php
```

<a name="data-properties-attributes"></a>
<!-- ### Data Properties / Attributes -->
### Data Properties / Attributes

<!-- Since anonymous components do not have any associated class, you may wonder how you may differentiate which data should be passed to the component as variables and which attributes should be placed in the component's [attribute bag](#component-attributes). -->
匿名コンポーネントには関連付けられたクラスがないため、どのデータを変数としてコンポーネントに渡す必要があるのか​​、またどの属性をコンポーネントの [attribute bag](#component-attributes) に配置する必要があるのか​​をどのように区別すればよいのか疑問に思うかもしれません。

<!-- You may specify which attributes should be considered data variables using the `@props` directive at the top of your component's Blade template. All other attributes on the component will be available via the component's attribute bag. If you wish to give a data variable a default value, you may specify the variable's name as the array key and the default value as the array value: -->
コンポーネントの Blade テンプレートの先頭にある `@props` ディレクティブを使用して、どの属性をデータ変数と見なすかを指定できます。コンポーネントの他のすべての属性は、コンポーネントの属性バッグを介して利用可能になります。データ変数にデフォルト値を与えたい場合は、変数の名前を配列キーとして指定し、デフォルト値を配列値として指定できます。

```blade
<!-- /resources/views/components/alert.blade.php -->

@props(['type' => 'info', 'message'])

<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

<!-- Given the component definition above, we may render the component like so: -->
上記のコンポーネント定義を考慮すると、次のようにコンポーネントをレンダリングできます。

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

<a name="accessing-parent-data"></a>
<!-- ### Accessing Parent Data -->
### Accessing Parent Data

<!-- Sometimes you may want to access data from a parent component inside a child component. In these cases, you may use the `@aware` directive. For example, imagine we are building a complex menu component consisting of a parent `<x-menu>` and child `<x-menu.item>`: -->
場合によっては、子コンポーネント内の親コンポーネントからデータにアクセスしたい場合があります。このような場合、`@aware` ディレクティブを使用できます。たとえば、親 `<x-menu>` と子 `<x-menu.item>` で構成される複雑なメニュー コンポーネントを構築していると想像してください。

```blade
<x-menu color="purple">
    <x-menu.item>...</x-menu.item>
    <x-menu.item>...</x-menu.item>
</x-menu>
```

<!-- The `<x-menu>` component may have an implementation like the following: -->
`<x-menu>` コンポーネントには、次のような実装が含まれる場合があります。

```blade
<!-- /resources/views/components/menu/index.blade.php -->

@props(['color' => 'gray'])

<ul {{ $attributes->merge(['class' => 'bg-'.$color.'-200']) }}>
    {{ $slot }}
</ul>
```

<!-- Because the `color` prop was only passed into the parent (`<x-menu>`), it won't be available inside `<x-menu.item>`. However, if we use the `@aware` directive, we can make it available inside `<x-menu.item>` as well: -->
`color` プロパティは親 (`<x-menu>`) にのみ渡されたため、`<x-menu.item>` 内では使用できません。ただし、`@aware` ディレクティブを使用すると、`<x-menu.item>` 内でも使用できるようになります。

```blade
<!-- /resources/views/components/menu/item.blade.php -->

@aware(['color' => 'gray'])

<li {{ $attributes->merge(['class' => 'text-'.$color.'-800']) }}>
    {{ $slot }}
</li>
```

> [!WARNING]
> `@aware` ディレクティブは、HTML 属性を介して親コンポーネントに明示的に渡されていない親データにはアクセスできません。親コンポーネントに明示的に渡されないデフォルトの `@props` 値には、`@aware` ディレクティブではアクセスできません。

<a name="anonymous-component-paths"></a>
<!-- ### Anonymous Component Paths -->
### Anonymous Component Paths

<!-- As previously discussed, anonymous components are typically defined by placing a Blade template within your `resources/views/components` directory. However, you may occasionally want to register other anonymous component paths with Laravel in addition to the default path. -->
前述したように、匿名コンポーネントは通常、`resources/views/components` ディレクトリ内に Blade テンプレートを配置することによって定義されます。ただし、デフォルトのパスに加えて、他の匿名コンポーネントのパスを Laravel に登録したい場合もあります。

<!-- The `anonymousComponentPath` method accepts the "path" to the anonymous component location as its first argument and an optional "namespace" that components should be placed under as its second argument. Typically, this method should be called from the `boot` method of one of your application's [service providers](/docs/10.x/providers): -->
`anonymousComponentPath` メソッドは、匿名コンポーネントの場所への「パス」を最初の引数として受け入れ、コンポーネントを配置する必要があるオプションの「名前空間」を 2 番目の引数として受け入れます。通常、このメソッドは、アプリケーションの [service providers](/docs/10.x/providers) の 1 つの `boot` メソッドから呼び出す必要があります。

```
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Blade::anonymousComponentPath(__DIR__.'/../components');
}
```

<!-- When component paths are registered without a specified prefix as in the example above, they may be rendered in your Blade components without a corresponding prefix as well. For example, if a `panel.blade.php` component exists in the path registered above, it may be rendered like so: -->
上記の例のように、コンポーネント パスがプレフィックスを指定せずに登録されている場合、Blade コンポーネントでも対応するプレフィックスなしでレンダリングされる可能性があります。たとえば、上記で登録したパスに `panel.blade.php` コンポーネントが存在する場合、次のようにレンダリングされます。

```blade
<x-panel />
```

<!-- Prefix "namespaces" may be provided as the second argument to the `anonymousComponentPath` method: -->
プレフィックス「namespaces」は、`anonymousComponentPath` メソッドの 2 番目の引数として指定できます。

```
Blade::anonymousComponentPath(__DIR__.'/../components', 'dashboard');
```

<!-- When a prefix is provided, components within that "namespace" may be rendered by prefixing to the component's namespace to the component name when the component is rendered: -->
プレフィックスが指定されている場合、コンポーネントがレンダリングされるときに、コンポーネントの名前空間にコンポーネント名をプレフィックスとして付けることによって、その「名前空間」内のコンポーネントがレンダリングされることがあります。

```blade
<x-dashboard::panel />
```

<a name="building-layouts"></a>
<!-- ## Building Layouts -->
## Building Layouts

<a name="layouts-using-components"></a>
<!-- ### Layouts Using Components -->
### Layouts Using Components

<!-- Most web applications maintain the same general layout across various pages. It would be incredibly cumbersome and hard to maintain our application if we had to repeat the entire layout HTML in every view we create. Thankfully, it's convenient to define this layout as a single [Blade component](#components) and then use it throughout our application. -->
ほとんどの Web アプリケーションは、さまざまなページにわたって同じ一般的なレイアウトを維持します。作成するすべてのビューでレイアウト HTML 全体を繰り返す必要がある場合、アプリケーションを保守するのは非常に面倒で困難になります。ありがたいことに、このレイアウトを単一の [Blade component](#components) として定義し、アプリケーション全体で使用すると便利です。

<a name="defining-the-layout-component"></a>
<!-- #### Defining the Layout Component -->
#### Defining the Layout Component

<!-- For example, imagine we are building a "todo" list application. We might define a `layout` component that looks like the following: -->
たとえば、「todo」リスト アプリケーションを構築していると想像してください。次のような `layout` コンポーネントを定義するとします。

```blade
<!-- resources/views/components/layout.blade.php -->

<html>
    <head>
        <title>{{ $title ?? 'Todo Manager' }}</title>
    </head>
    <body>
        <h1>Todos</h1>
        <hr/>
        {{ $slot }}
    </body>
</html>
```

<a name="applying-the-layout-component"></a>
<!-- #### Applying the Layout Component -->
#### Applying the Layout Component

<!-- Once the `layout` component has been defined, we may create a Blade view that utilizes the component. In this example, we will define a simple view that displays our task list: -->
`layout` コンポーネントが定義されたら、そのコンポーネントを利用するBlade ビューを作成できます。この例では、タスク リストを表示する単純なビューを定義します。

```blade
<!-- resources/views/tasks.blade.php -->

<x-layout>
    @foreach ($tasks as $task)
        {{ $task }}
    @endforeach
</x-layout>
```

<!-- Remember, content that is injected into a component will be supplied to the default `$slot` variable within our `layout` component. As you may have noticed, our `layout` also respects a `$title` slot if one is provided; otherwise, a default title is shown. We may inject a custom title from our task list view using the standard slot syntax discussed in the [component documentation](#components): -->
コンポーネントに挿入されるコンテンツは、`layout` コンポーネント内のデフォルトの `$slot` 変数に提供されることに注意してください。お気づきかもしれませんが、`layout` は、`$title` スロットが提供されている場合はそれも尊重します。それ以外の場合は、デフォルトのタイトルが表示されます。 [component documentation](#components) で説明されている標準スロット構文を使用して、タスク リスト ビューからカスタム タイトルを挿入できます。

```blade
<!-- resources/views/tasks.blade.php -->

<x-layout>
    <x-slot:title>
        Custom Title
    </x-slot>

    @foreach ($tasks as $task)
        {{ $task }}
    @endforeach
</x-layout>
```

<!-- Now that we have defined our layout and task list views, we just need to return the `task` view from a route: -->
レイアウト ビューとタスク リスト ビューを定義したので、あとはルートから `task` ビューを返すだけです。

```
use App\Models\Task;

Route::get('/tasks', function () {
    return view('tasks', ['tasks' => Task::all()]);
});
```

<a name="layouts-using-template-inheritance"></a>
<!-- ### Layouts Using Template Inheritance -->
### Layouts Using Template Inheritance

<a name="defining-a-layout"></a>
<!-- #### Defining a Layout -->
#### Defining a Layout

<!-- Layouts may also be created via "template inheritance". This was the primary way of building applications prior to the introduction of [components](#components). -->
レイアウトは「テンプレートの継承」によって作成することもできます。これは、[components](#components) が導入される前は、アプリケーションを構築する主な方法でした。

<!-- To get started, let's take a look at a simple example. First, we will examine a page layout. Since most web applications maintain the same general layout across various pages, it's convenient to define this layout as a single Blade view: -->
まず、簡単な例を見てみましょう。まず、ページ レイアウトを検討します。ほとんどの Web アプリケーションはさまざまなページにわたって同じ一般的なレイアウトを維持するため、このレイアウトを単一のBlade ビューとして定義すると便利です。

```blade
<!-- resources/views/layouts/app.blade.php -->

<html>
    <head>
        <title>App Name - @yield('title')</title>
    </head>
    <body>
        @section('sidebar')
            This is the master sidebar.
        @show

        <div class="container">
            @yield('content')
        </div>
    </body>
</html>
```

<!-- As you can see, this file contains typical HTML mark-up. However, take note of the `@section` and `@yield` directives. The `@section` directive, as the name implies, defines a section of content, while the `@yield` directive is used to display the contents of a given section. -->
ご覧のとおり、このファイルには典型的な HTML マークアップが含まれています。ただし、`@section` ディレクティブと `@yield` ディレクティブに注意してください。 `@section` ディレクティブは、名前が示すとおり、コンテンツのセクションを定義します。一方、`@yield` ディレクティブは、特定のセクションのコンテンツを表示するために使用されます。

<!-- Now that we have defined a layout for our application, let's define a child page that inherits the layout. -->
アプリケーションのレイアウトを定義したので、そのレイアウトを継承する子ページを定義しましょう。

<a name="extending-a-layout"></a>
<!-- #### Extending a Layout -->
#### Extending a Layout

<!-- When defining a child view, use the `@extends` Blade directive to specify which layout the child view should "inherit". Views which extend a Blade layout may inject content into the layout's sections using `@section` directives. Remember, as seen in the example above, the contents of these sections will be displayed in the layout using `@yield`: -->
子ビューを定義するときは、`@extends` Blade ディレクティブを使用して、子ビューが「継承」するレイアウトを指定します。Blade レイアウトを拡張するビューは、`@section` ディレクティブを使用してレイアウトのセクションにコンテンツを挿入できます。上の例にあるように、これらのセクションの内容は、`@yield` を使用してレイアウトに表示されることに注意してください。

```blade
<!-- resources/views/child.blade.php -->

@extends('layouts.app')

@section('title', 'Page Title')

@section('sidebar')
    @@parent

    <p>This is appended to the master sidebar.</p>
@endsection

@section('content')
    <p>This is my body content.</p>
@endsection
```

<!-- In this example, the `sidebar` section is utilizing the `@@parent` directive to append (rather than overwriting) content to the layout's sidebar. The `@@parent` directive will be replaced by the content of the layout when the view is rendered. -->
この例では、`sidebar` セクションは `@@parent` ディレクティブを利用して、レイアウトのサイドバーにコンテンツを (上書きではなく) 追加しています。 `@@parent` ディレクティブは、ビューがレンダリングされるときにレイアウトのコンテンツに置き換えられます。

> [!NOTE]
> 前の例とは異なり、この `sidebar` セクションは、`@show` ではなく `@endsection` で終わります。 `@endsection` ディレクティブはセクションを定義するだけですが、`@show` はセクションを定義して **即座に生成**します。

<!-- The `@yield` directive also accepts a default value as its second parameter. This value will be rendered if the section being yielded is undefined: -->
`@yield` ディレクティブは、2 番目のパラメーターとしてデフォルト値も受け入れます。この値は、生成されるセクションが未定義の場合に表示されます。

```blade
@yield('content', 'Default content')
```

<a name="forms"></a>
<!-- ## Forms -->
## Forms

<a name="csrf-field"></a>
<!-- ### CSRF Field -->
### CSRF Field

<!-- Anytime you define an HTML form in your application, you should include a hidden CSRF token field in the form so that [the CSRF protection](/docs/10.x/csrf) middleware can validate the request. You may use the `@csrf` Blade directive to generate the token field: -->
アプリケーションで HTML フォームを定義するときは常に、[the CSRF protection](/docs/10.x/csrf) ミドルウェアがリクエストを検証できるように、フォームに非表示の CSRF トークン フィールドを含める必要があります。 `@csrf` Blade ディレクティブを使用してトークン フィールドを生成できます。

```blade
<form method="POST" action="/profile">
    @csrf

    ...
</form>
```

<a name="method-field"></a>
<!-- ### Method Field -->
### Method Field

<!-- Since HTML forms can't make `PUT`, `PATCH`, or `DELETE` requests, you will need to add a hidden `_method` field to spoof these HTTP verbs. The `@method` Blade directive can create this field for you: -->
HTML フォームは `PUT`、`PATCH`、または `DELETE` リクエストを作成できないため、これらの HTTP 動詞を偽装するには、非表示の `_method` フィールドを追加する必要があります。 `@method` Blade ディレクティブは、このフィールドを作成できます。

```blade
<form action="/foo/bar" method="POST">
    @method('PUT')

    ...
</form>
```

<a name="validation-errors"></a>
<!-- ### Validation Errors -->
### Validation Errors

<!-- The `@error` directive may be used to quickly check if [validation error messages](/docs/10.x/validation#quick-displaying-the-validation-errors) exist for a given attribute. Within an `@error` directive, you may echo the `$message` variable to display the error message: -->
`@error` ディレクティブを使用すると、特定の属性に [validation error messages](/docs/10.x/validation#quick-displaying-the-validation-errors) が存在するかどうかをすばやく確認できます。 `@error` ディレクティブ内で、`$message` 変数をエコーし​​てエラー メッセージを表示できます。

```blade
<!-- /resources/views/post/create.blade.php -->

<label for="title">Post Title</label>

<input id="title"
    type="text"
    class="@error('title') is-invalid @enderror">

@error('title')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```

<!-- Since the `@error` directive compiles to an "if" statement, you may use the `@else` directive to render content when there is not an error for an attribute: -->
`@error` ディレクティブは「if」ステートメントにコンパイルされるため、属性にエラーがない場合は、`@else` ディレクティブを使用してコンテンツをレンダリングできます。

```blade
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input id="email"
    type="email"
    class="@error('email') is-invalid @else is-valid @enderror">
```

<!-- You may pass [the name of a specific error bag](/docs/10.x/validation#named-error-bags) as the second parameter to the `@error` directive to retrieve validation error messages on pages containing multiple forms: -->
[the name of a specific error bag](/docs/10.x/validation#named-error-bags) を `@error` ディレクティブの 2 番目のパラメーターとして渡して、複数のフォームを含むページの検証エラー メッセージを取得できます。

```blade
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input id="email"
    type="email"
    class="@error('email', 'login') is-invalid @enderror">

@error('email', 'login')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```

<a name="stacks"></a>
<!-- ## Stacks -->
## Stacks

<!-- Blade allows you to push to named stacks which can be rendered somewhere else in another view or layout. This can be particularly useful for specifying any JavaScript libraries required by your child views: -->
Blade を使用すると、別のビューまたはレイアウトの別の場所にレンダリングできる名前付きスタックにプッシュできます。これは、子ビューで必要な JavaScript ライブラリを指定する場合に特に役立ちます。

```blade
@push('scripts')
    <script src="/example.js"></script>
@endpush
```

<!-- If you would like to `@push` content if a given boolean expression evaluates to `true`, you may use the `@pushIf` directive: -->
指定されたブール式が `true` と評価された場合に `@push` コンテンツを取得したい場合は、`@pushIf` ディレクティブを使用できます。

```blade
@pushIf($shouldPush, 'scripts')
    <script src="/example.js"></script>
@endPushIf
```

<!-- You may push to a stack as many times as needed. To render the complete stack contents, pass the name of the stack to the `@stack` directive: -->
必要に応じて何度でもスタックにプッシュできます。完全なスタックの内容をレンダリングするには、スタックの名前を `@stack` ディレクティブに渡します。

```blade
<head>
    <!-- Head Contents -->

    @stack('scripts')
</head>
```

<!-- If you would like to prepend content onto the beginning of a stack, you should use the `@prepend` directive: -->
コンテンツをスタックの先頭に追加したい場合は、`@prepend` ディレクティブを使用する必要があります。

```blade
@push('scripts')
    This will be second...
@endpush

// Later...

@prepend('scripts')
    This will be first...
@endprepend
```

<a name="service-injection"></a>
<!-- ## Service Injection -->
## Service Injection

<!-- The `@inject` directive may be used to retrieve a service from the Laravel [service container](/docs/10.x/container). The first argument passed to `@inject` is the name of the variable the service will be placed into, while the second argument is the class or interface name of the service you wish to resolve: -->
`@inject` ディレクティブは、Laravel [service container](/docs/10.x/container) からサービスを取得するために使用できます。 `@inject` に渡される最初の引数はサービスが配置される変数の名前であり、2 番目の引数は解決するサービスのクラス名またはインターフェイス名です。

```blade
@inject('metrics', 'App\Services\MetricsService')

<div>
    Monthly Revenue: {{ $metrics->monthlyRevenue() }}.
</div>
```

<a name="rendering-inline-blade-templates"></a>
<!-- ## Rendering Inline Blade Templates -->
## Rendering Inline Blade Templates

<!-- Sometimes you may need to transform a raw Blade template string into valid HTML. You may accomplish this using the `render` method provided by the `Blade` facade. The `render` method accepts the Blade template string and an optional array of data to provide to the template: -->
場合によっては、生の Blade テンプレート文字列を有効な HTML に変換する必要があるかもしれません。これは、`Blade` ファサードによって提供される `render` メソッドを使用して実行できます。 `render` メソッドは、Blade テンプレート文字列と、テンプレートに提供するオプションのデータ配列を受け入れます。

```php
use Illuminate\Support\Facades\Blade;

return Blade::render('Hello, {{ $name }}', ['name' => 'Julian Bashir']);
```

<!-- Laravel renders inline Blade templates by writing them to the `storage/framework/views` directory. If you would like Laravel to remove these temporary files after rendering the Blade template, you may provide the `deleteCachedView` argument to the method: -->
Laravel は、インライン Blade テンプレートを `storage/framework/views` ディレクトリに書き込むことでレンダリングします。 Blade テンプレートのレンダリング後に Laravel にこれらの一時ファイルを削除させたい場合は、メソッドに `deleteCachedView` 引数を指定できます。

```php
return Blade::render(
    'Hello, {{ $name }}',
    ['name' => 'Julian Bashir'],
    deleteCachedView: true
);
```

<a name="rendering-blade-fragments"></a>
<!-- ## Rendering Blade Fragments -->
## Rendering Blade Fragments

<!-- When using frontend frameworks such as [Turbo](https://turbo.hotwired.dev/) and [htmx](https://htmx.org/), you may occasionally need to only return a portion of a Blade template within your HTTP response. Blade "fragments" allow you to do just that. To get started, place a portion of your Blade template within `@fragment` and `@endfragment` directives: -->
[Turbo](https://turbo.hotwired.dev/) や [htmx](https://htmx.org/) などのフロントエンド フレームワークを使用する場合、HTTP 応答内で Blade テンプレートの一部のみを返す必要がある場合があります。Bladeの「フラグメント」を使用すると、まさにそれが可能になります。まず、Blade テンプレートの一部を `@fragment` および `@endfragment` ディレクティブ内に配置します。

```blade
@fragment('user-list')
    <ul>
        @foreach ($users as $user)
            <li>{{ $user->name }}</li>
        @endforeach
    </ul>
@endfragment
```

<!-- Then, when rendering the view that utilizes this template, you may invoke the `fragment` method to specify that only the specified fragment should be included in the outgoing HTTP response: -->
次に、このテンプレートを利用するビューをレンダリングするときに、`fragment` メソッドを呼び出して、指定されたフラグメントのみが送信 HTTP 応答に含まれるように指定できます。

```php
return view('dashboard', ['users' => $users])->fragment('user-list');
```

<!-- The `fragmentIf` method allows you to conditionally return a fragment of a view based on a given condition. Otherwise, the entire view will be returned: -->
`fragmentIf` メソッドを使用すると、指定された条件に基づいてビューのフラグメントを条件付きで返すことができます。それ以外の場合は、ビュー全体が返されます。

```php
return view('dashboard', ['users' => $users])
    ->fragmentIf($request->hasHeader('HX-Request'), 'user-list');
```

<!-- The `fragments` and `fragmentsIf` methods allow you to return multiple view fragments in the response. The fragments will be concatenated together: -->
`fragments` メソッドと `fragmentsIf` メソッドを使用すると、応答で複数のビュー フラグメントを返すことができます。フラグメントは連結されます。

```php
view('dashboard', ['users' => $users])
    ->fragments(['user-list', 'comment-list']);

view('dashboard', ['users' => $users])
    ->fragmentsIf(
        $request->hasHeader('HX-Request'),
        ['user-list', 'comment-list']
    );
```

<a name="extending-blade"></a>
<!-- ## Extending Blade -->
## Extending Blade

<!-- Blade allows you to define your own custom directives using the `directive` method. When the Blade compiler encounters the custom directive, it will call the provided callback with the expression that the directive contains. -->
Blade では、`directive` メソッドを使用して独自のカスタム ディレクティブを定義できます。 Blade コンパイラはカスタム ディレクティブを検出すると、ディレクティブに含まれる式を使用して提供されたコールバックを呼び出します。

<!-- The following example creates a `@datetime($var)` directive which formats a given `$var`, which should be an instance of `DateTime`: -->
次の例では、指定された `$var` をフォーマットする `@datetime($var)` ディレクティブを作成します。これは、`DateTime` のインスタンスである必要があります。

```
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Blade;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Blade::directive('datetime', function (string $expression) {
            return "<?php echo ($expression)->format('m/d/Y H:i'); ?>";
        });
    }
}
```

<!-- As you can see, we will chain the `format` method onto whatever expression is passed into the directive. So, in this example, the final PHP generated by this directive will be: -->
ご覧のとおり、ディレクティブに渡される式に `format` メソッドを連鎖させます。したがって、この例では、このディレクティブによって生成される最終的な PHP は次のようになります。

```
<?php echo ($var)->format('m/d/Y H:i'); ?>
```

> [!WARNING]
> Blade ディレクティブのロジックを更新した後、キャッシュされた Blade ビューをすべて削除する必要があります。キャッシュされたBlade ビューは、`view:clear` Artisan コマンドを使用して削除できます。

<a name="custom-echo-handlers"></a>
<!-- ### Custom Echo Handlers -->
### Custom Echo Handlers

<!-- If you attempt to "echo" an object using Blade, the object's `__toString` method will be invoked. The [`__toString`](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) method is one of PHP's built-in "magic methods". However, sometimes you may not have control over the `__toString` method of a given class, such as when the class that you are interacting with belongs to a third-party library. -->
Blade を使用してオブジェクトを「エコー」しようとすると、オブジェクトの `__toString` メソッドが呼び出されます。 [`__toString`](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) メソッドは、PHP の組み込み「マジック メソッド」の 1 つです。ただし、対話しているクラスがサードパーティのライブラリに属している場合など、特定のクラスの `__toString` メソッドを制御できない場合があります。

<!-- In these cases, Blade allows you to register a custom echo handler for that particular type of object. To accomplish this, you should invoke Blade's `stringable` method. The `stringable` method accepts a closure. This closure should type-hint the type of object that it is responsible for rendering. Typically, the `stringable` method should be invoked within the `boot` method of your application's `AppServiceProvider` class: -->
このような場合、Blade では、その特定の種類のオブジェクトにカスタム エコー ハンドラーを登録できます。これを実現するには、Blade の `stringable` メソッドを呼び出す必要があります。 `stringable` メソッドはクロージャを受け入れます。このクロージャは、レンダリングを担当するオブジェクトのタイプをタイプヒントする必要があります。通常、`stringable` メソッドは、アプリケーションの `AppServiceProvider` クラスの `boot` メソッド内で呼び出す必要があります。

```
use Illuminate\Support\Facades\Blade;
use Money\Money;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Blade::stringable(function (Money $money) {
        return $money->formatTo('en_GB');
    });
}
```

<!-- Once your custom echo handler has been defined, you may simply echo the object in your Blade template: -->
カスタム エコー ハンドラーを定義したら、Blade テンプレート内のオブジェクトをエコーするだけです。

```blade
Cost: {{ $money }}
```

<a name="custom-if-statements"></a>
<!-- ### Custom If Statements -->
### Custom If Statements

<!-- Programming a custom directive is sometimes more complex than necessary when defining simple, custom conditional statements. For that reason, Blade provides a `Blade::if` method which allows you to quickly define custom conditional directives using closures. For example, let's define a custom conditional that checks the configured default "disk" for the application. We may do this in the `boot` method of our `AppServiceProvider`: -->
カスタム ディレクティブのプログラミングは、単純なカスタム条件文を定義する場合、必要以上に複雑になる場合があります。そのため、Blade は、クロージャを使用してカスタム条件ディレクティブを迅速に定義できる `Blade::if` メソッドを提供します。たとえば、アプリケーションに設定されたデフォルトの「ディスク」をチェックするカスタム条件を定義してみましょう。これは、`AppServiceProvider` の `boot` メソッドで行うことができます。

```
use Illuminate\Support\Facades\Blade;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Blade::if('disk', function (string $value) {
        return config('filesystems.default') === $value;
    });
}
```

<!-- Once the custom conditional has been defined, you can use it within your templates: -->
カスタム条件を定義したら、それをテンプレート内で使用できます。

```blade
@disk('local')
    <!-- The application is using the local disk... -->
@elsedisk('s3')
    <!-- The application is using the s3 disk... -->
@else
    <!-- The application is using some other disk... -->
@enddisk

@unlessdisk('local')
    <!-- The application is not using the local disk... -->
@enddisk
```

