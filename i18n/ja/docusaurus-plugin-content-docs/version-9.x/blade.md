# Blade テンプレート (Blade Templates)

- [Introduction](#introduction)
    - [Livewireを備えたスーパーチャージャーBlade](#supercharging-blade-with-livewire)
- [データの表示](#displaying-data)
    - [HTMLエンティティのエンコーディング](#html-entity-encoding)
    - [Bladeと JavaScript フレームワーク](#blade-and-javascript-frameworks)
- [Blade ディレクティブ](#blade-directives)
    - [If ステートメント](#if-statements)
    - [スイッチステートメント](#switch-statements)
    - [Loops](#loops)
    - [ループ変数](#the-loop-variable)
    - [条件付きクラス](#conditional-classes)
    - [追加の属性](#additional-attributes)
    - [サブビューを含む](#including-subviews)
    - [`@once` ディレクティブ](#the-once-directive)
    - [生のPHP](#raw-php)
    - [Comments](#comments)
- [Components](#components)
    - [レンダリングコンポーネント](#rendering-components)
    - [コンポーネントにデータを渡す](#passing-data-to-components)
    - [コンポーネントの属性](#component-attributes)
    - [予約されたキーワード](#reserved-keywords)
    - [Slots](#slots)
    - [インラインコンポーネントビュー](#inline-component-views)
    - [動的コンポーネント](#dynamic-components)
    - [コンポーネントを手動で登録する](#manually-registering-components)
- [匿名コンポーネント](#anonymous-components)
    - [匿名インデックスコンポーネント](#anonymous-index-components)
    - [データのプロパティ/属性](#data-properties-attributes)
    - [親データへのアクセス](#accessing-parent-data)
    - [匿名コンポーネントのパス](#anonymous-component-paths)
- [建物のレイアウト](#building-layouts)
    - [コンポーネントを使用したレイアウト](#layouts-using-components)
    - [テンプレートの継承を使用したレイアウト](#layouts-using-template-inheritance)
- [Forms](#forms)
    - [CSRFフィールド](#csrf-field)
    - [メソッドフィールド](#method-field)
    - [検証エラー](#validation-errors)
- [Stacks](#stacks)
- [サービスインジェクション](#service-injection)
- [インラインBlade テンプレートのレンダリング](#rendering-inline-blade-templates)
- [刃の破片のレンダリング](#rendering-blade-fragments)
- [伸びる刃](#extending-blade)
    - [カスタム エコー ハンドラー](#custom-echo-handlers)
    - [カスタムの If ステートメント](#custom-if-statements)

<a name="introduction"></a>
## 導入 (Introduction)

Blade は、Laravel に含まれるシンプルかつ強力なテンプレート エンジンです。一部の PHP テンプレート エンジンとは異なり、Blade では、テンプレート内でプレーンな PHP コードを使用することが制限されません。実際、すべての Blade テンプレートはプレーンな PHP コードにコンパイルされ、変更されるまでキャッシュされます。つまり、Blade はアプリケーションに本質的にオーバーヘッドを追加しません。Blade テンプレート ファイルは、`.blade.php` ファイル拡張子を使用し、通常は `resources/views` ディレクトリに保存されます。

Blade ビューは、グローバル `view` ヘルパを使用してルートまたはコントローラから返される場合があります。もちろん、[views](/docs/{{version}}/views) のドキュメントで説明されているように、`view` ヘルパの 2 番目の引数を使用してデータをBlade ビューに渡すこともできます。

    Route::get('/', function () {
        return view('greeting', ['name' => 'Finn']);
    });

<a name="supercharging-blade-with-livewire"></a>
### Livewireを備えたスーパーチャージャーBlade

Blade テンプレートを次のレベルに引き上げて、動的なインターフェイスを簡単に構築したいですか? [Laravel Livewire](https://laravel-livewire.com) をチェックしてください。 Livewire を使用すると、通常は React や Vue などのフロントエンド フレームワークを介してのみ可能となる動的機能で拡張された Blade コンポーネントを作成でき、多くの JavaScript フレームワークの複雑さ、クライアント側のレンダリング、ビルド手順を必要とせずに、最新のリアクティブ フロントエンドを構築するための優れたアプローチを提供します。

<a name="displaying-data"></a>
## データの表示 (Displaying Data)

変数を中括弧で囲むことにより、Blade ビューに渡されるデータを表示できます。たとえば、次のルートがあるとします。

    Route::get('/', function () {
        return view('welcome', ['name' => 'Samantha']);
    });

次のように `name` 変数の内容を表示できます。

```blade
Hello, {{ $name }}.
```

> **注記**
> Blade の `{{ }}` エコー ステートメントは、PHP の `htmlspecialchars` 関数を通じて自動的に送信され、XSS 攻撃を防ぎます。

ビューに渡された変数の内容を表示することに限定されません。任意の PHP 関数の結果をエコーすることもできます。実際、Blade echo ステートメント内に任意の PHP コードを含めることができます。

```blade
The current UNIX timestamp is {{ time() }}.
```

<a name="html-entity-encoding"></a>
### HTMLエンティティのエンコーディング

デフォルトでは、Blade (および Laravel `e` ヘルパ) は HTML エンティティを二重エンコードします。二重エンコードを無効にしたい場合は、`AppServiceProvider` の `boot` メソッドから `Blade::withoutDoubleEncoding` メソッドを呼び出します。

    <?php

    namespace App\Providers;

    use Illuminate\Support\Facades\Blade;
    use Illuminate\Support\ServiceProvider;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * Bootstrap any application services.
         *
         * @return void
         */
        public function boot()
        {
            Blade::withoutDoubleEncoding();
        }
    }

<a name="displaying-unescaped-data"></a>
#### エスケープされていないデータの表示

デフォルトでは、Bladeの `{{ }}` ステートメントは、XSS 攻撃を防ぐために、PHP の `htmlspecialchars` 関数を通じて自動的に送信されます。データをエスケープしたくない場合は、次の構文を使用できます。

```blade
Hello, {!! $name !!}.
```

> **警告**
> アプリケーションのユーザーが提供したコンテンツをエコーする場合は、十分に注意してください。ユーザーが指定したデータを表示するときに XSS 攻撃を防ぐには、通常、エスケープされた二重中括弧構文を使用する必要があります。

<a name="blade-and-javascript-frameworks"></a>
### Bladeと JavaScript フレームワーク

多くの JavaScript フレームワークでも、特定の式をブラウザーに表示する必要があることを示すために「中括弧」を使用するため、`@` シンボルを使用して、式をそのままにしておく必要があることを Blade レンダリング エンジンに通知できます。例えば：

```blade
<h1>Laravel</h1>

Hello, @{{ name }}.
```

この例では、`@` シンボルが Blade によって削除されます。ただし、`{{ name }}` 式は Blade エンジンによって変更されないため、JavaScript フレームワークによってレンダリングできます。

`@` シンボルは、Blade ディレクティブをエスケープするために使用することもできます。

```blade
{{-- Blade template --}}
@@if()

<!-- HTML output -->
@if()
```

<a name="rendering-json"></a>
#### JSONのレンダリング

JavaScript 変数を初期化するために、配列を JSON としてレンダリングする目的でビューに配列を渡すことがあります。例えば：

```blade
<script>
    var app = <?php echo json_encode($array); ?>;
</script>
```

ただし、`json_encode` を手動で呼び出す代わりに、`Illuminate\Support\Js::from` メソッド ディレクティブを使用することもできます。 `from` メソッドは、PHP の `json_encode` 関数と同じ引数を受け入れます。ただし、結果の JSON が HTML 引用符内に含められるように適切にエスケープされることが保証されます。 `from` メソッドは、指定されたオブジェクトまたは配列を有効な JavaScript オブジェクトに変換する文字列 `JSON.parse` JavaScript ステートメントを返します。

```blade
<script>
    var app = {{ Illuminate\Support\Js::from($array) }};
</script>
```

Laravel アプリケーション スケルトンの最新バージョンには、Blade テンプレート内のこの機能への便利なアクセスを提供する `Js` ファサードが含まれています。

```blade
<script>
    var app = {{ Js::from($array) }};
</script>
```

> **警告**
> 既存の変数を JSON としてレンダリングする場合は、`Js::from` メソッドのみを使用してください。 Blade テンプレートは正規表現に基づいており、複雑な表現をディレクティブに渡そうとすると、予期しないエラーが発生する可能性があります。

<a name="the-at-verbatim-directive"></a>
#### `@verbatim` ディレクティブ

テンプレートの大部分で JavaScript 変数を表示している場合は、HTML を `@verbatim` ディレクティブでラップすると、各 Blade echo ステートメントの前に `@` シンボルを付ける必要がなくなります。

```blade
@verbatim
    <div class="container">
        Hello, {{ name }}.
    </div>
@endverbatim
```

<a name="blade-directives"></a>
## Blade ディレクティブ (Blade Directives)

Blade は、テンプレートの継承とデータの表示に加えて、条件ステートメントやループなどの一般的な PHP 制御構造の便利なショートカットも提供します。これらのショートカットは、PHP の制御構造を操作するための非常にクリーンで簡潔な方法を提供すると同時に、PHP の対応するものにとっても馴染みのあるものです。

<a name="if-statements"></a>
### If ステートメント

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

便宜上、Blade には `@unless` ディレクティブも用意されています。

```blade
@unless (Auth::check())
    You are not signed in.
@endunless
```

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
#### 認証ディレクティブ

`@auth` および `@guest` ディレクティブを使用すると、現在のユーザーが [authenticated](/docs/{{version}}/authentication) であるかゲストであるかを迅速に判断できます。

```blade
@auth
    // The user is authenticated...
@endauth

@guest
    // The user is not authenticated...
@endguest
```

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
#### 環境指令

`@production` ディレクティブを使用して、アプリケーションが運用環境で実行されているかどうかを確認できます。

```blade
@production
    // Production specific content...
@endproduction
```

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
#### セクションディレクティブ

`@hasSection` ディレクティブを使用して、テンプレート継承セクションにコンテンツがあるかどうかを判断できます。

```blade
@hasSection('navigation')
    <div class="pull-right">
        @yield('navigation')
    </div>

    <div class="clearfix"></div>
@endif
```

`@sectionMissing` ディレクティブを使用して、セクションにコンテンツがないかどうかを判断できます。

```blade
@sectionMissing('navigation')
    <div class="pull-right">
        @include('default-navigation')
    </div>
@endif
```

<a name="switch-statements"></a>
### スイッチステートメント

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
### ループ

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

> **注記**
> `foreach` ループを反復しているときに、[ループ変数](#the-loop-variable) を使用して、ループの最初の反復にいるか最後の反復にいるかなど、ループに関する貴重な情報を取得できます。

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

ディレクティブ宣言内に継続条件または中断条件を含めることもできます。

```blade
@foreach ($users as $user)
    @continue($user->type == 1)

    <li>{{ $user->name }}</li>

    @break($user->number == 5)
@endforeach
```

<a name="the-loop-variable"></a>
### ループ変数

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

`$loop` 変数には、他にもさまざまな便利なプロパティが含まれています。

| 財産           | 説明                                            |
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
### 条件付きクラスとスタイル

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
### 追加の属性

便宜上、`@checked` ディレクティブを使用して、特定の HTML チェックボックス入力が「チェックされている」かどうかを簡単に示すことができます。このディレクティブは、指定された条件が `true` と評価される場合、`checked` をエコーし​​ます。

```blade
<input type="checkbox"
        name="active"
        value="active"
        @checked(old('active', $user->active)) />
```

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

さらに、`@disabled` ディレクティブを使用して、特定の要素を「無効」にするかどうかを示すことができます。

```blade
<button type="submit" @disabled($errors->isNotEmpty())>Submit</button>
```

さらに、`@readonly` ディレクティブを使用して、特定の要素を「読み取り専用」にするかどうかを示すことができます。

```blade
<input type="email"
        name="email"
        value="email@laravel.com"
        @readonly($user->isNotAdmin()) />
```

さらに、`@required` ディレクティブを使用して、特定の要素が「必須」であるかどうかを示すことができます。

```blade
<input type="text"
        name="title"
        value="title"
        @required($user->isAdmin()) />
```

<a name="including-subviews"></a>
### サブビューを含む

> **注記**
> `@include` ディレクティブは自由に使用できますが、Blade [components](#components) は同様の機能を提供し、データや属性のバインディングなど、`@include` ディレクティブよりも優れたいくつかの利点を提供します。

Blade の `@include` ディレクティブを使用すると、別のビュー内から Blade ビューを含めることができます。親ビューで使用できるすべての変数は、組み込まれたビューでも使用できるようになります。

```blade
<div>
    @include('shared.errors')

    <form>
        <!-- Form Contents -->
    </form>
</div>
```

含まれるビューは親ビューで使用可能なすべてのデータを継承しますが、含まれるビューで使用できるようにする必要がある追加データの配列を渡すこともできます。

```blade
@include('view.name', ['status' => 'complete'])
```

存在しないビューを `@include` しようとすると、Laravel はエラーをスローします。存在するかどうかわからないビューを含めたい場合は、`@includeIf` ディレクティブを使用する必要があります。

```blade
@includeIf('view.name', ['status' => 'complete'])
```

指定されたブール式が `true` または `false` に評価される場合にビューを `@include` したい場合は、`@includeWhen` および `@includeUnless` ディレクティブを使用できます。

```blade
@includeWhen($boolean, 'view.name', ['status' => 'complete'])

@includeUnless($boolean, 'view.name', ['status' => 'complete'])
```

指定されたビューの配列から存在する最初のビューを含めるには、`@includeFirst` ディレクティブを使用できます。

```blade
@includeFirst(['custom.admin', 'admin'], ['status' => 'complete'])
```

> **警告**
> Blade ビューでは、`__DIR__` 定数と `__FILE__` 定数を使用しないでください。これらの定数は、キャッシュされコンパイルされたビューの場所を参照するためです。

<a name="rendering-views-for-collections"></a>
#### コレクションのビューのレンダリング

Blade の `@each` ディレクティブを使用して、ループとインクルードを 1 行に結合できます。

```blade
@each('view.name', $jobs, 'job')
```

`@each` ディレクティブの最初の引数は、配列またはコレクション内の各要素に対してレンダリングするビューです。 2 番目の引数は反復処理する配列またはコレクションで、3 番目の引数はビュー内の現在の反復に割り当てられる変数名です。したがって、たとえば、`jobs` の配列を反復処理している場合、通常はビュー内の `job` 変数として各ジョブにアクセスする必要があります。現在の反復の配列キーは、ビュー内の `key` 変数として使用できます。

`@each` ディレクティブに 4 番目の引数を渡すこともできます。この引数は、指定された配列が空の場合にレンダリングされるビューを決定します。

```blade
@each('view.name', $jobs, 'job', 'view.empty')
```

> **警告**
> `@each` を介してレンダリングされたビューは、親ビューから変数を継承しません。子ビューでこれらの変数が必要な場合は、代わりに `@foreach` および `@include` ディレクティブを使用する必要があります。

<a name="the-once-directive"></a>
### `@once` ディレクティブ

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

`@once` ディレクティブは、`@push` または `@prepend` ディレクティブと組み合わせて使用​​されることが多いため、便宜のために `@pushOnce` および `@prependOnce` ディレクティブを使用できます。

```blade
@pushOnce('scripts')
    <script>
        // Your custom JavaScript...
    </script>
@endPushOnce
```

<a name="raw-php"></a>
### 生のPHP

状況によっては、PHP コードをビューに埋め込むと便利です。 Blade `@php` ディレクティブを使用して、テンプレート内のプレーン PHP のブロックを実行できます。

```blade
@php
    $counter = 1;
@endphp
```

単一の PHP ステートメントのみを記述する必要がある場合は、そのステートメントを `@php` ディレクティブ内に含めることができます。

```blade
@php($counter = 1)
```

<a name="comments"></a>
### コメント

Blade では、ビュー内にコメントを定義することもできます。ただし、HTML コメントとは異なり、Blade コメントはアプリケーションから返される HTML には含まれません。

```blade
{{-- This comment will not be present in the rendered HTML --}}
```

<a name="components"></a>
## コンポーネント (Components)

コンポーネントとスロットは、セクション、レイアウト、インクルードに同様の利点をもたらします。ただし、コンポーネントとスロットのメンタル モデルの方が理解しやすいと感じる人もいるかもしれません。コンポーネントを作成するには、クラスベースのコンポーネントと匿名コンポーネントの 2 つのアプローチがあります。

クラスベースのコンポーネントを作成するには、`make:component` Artisan コマンドを使用できます。コンポーネントの使用方法を説明するために、単純な `Alert` コンポーネントを作成します。 `make:component` コマンドは、コンポーネントを `app/View/Components` ディレクトリに配置します。

```shell
php artisan make:component Alert
```

`make:component` コマンドは、コンポーネントのビュー テンプレートも作成します。ビューは `resources/views/components` ディレクトリに配置されます。独自のアプリケーションのコンポーネントを作成する場合、コンポーネントは `app/View/Components` ディレクトリおよび `resources/views/components` ディレクトリ内で自動的に検出されるため、通常は追加のコンポーネントの登録は必要ありません。

サブディレクトリ内にコンポーネントを作成することもできます。

```shell
php artisan make:component Forms/Input
```

上記のコマンドは、`app/View/Components/Forms` ディレクトリに `Input` コンポーネントを作成し、ビューは `resources/views/components/forms` ディレクトリに配置されます。

匿名コンポーネント (Blade テンプレートのみでクラスを持たないコンポーネント) を作成する場合は、`make:component` コマンドを呼び出すときに `--view` フラグを使用できます。

```shell
php artisan make:component forms.input --view
```

上記のコマンドは、`resources/views/components/forms/input.blade.php` に Blade ファイルを作成し、`<x-forms.input />` を介してコンポーネントとしてレンダリングできます。

<a name="manually-registering-package-components"></a>
#### パッケージコンポーネントの手動登録

独自のアプリケーションのコンポーネントを作成する場合、コンポーネントは `app/View/Components` ディレクトリおよび `resources/views/components` ディレクトリ内で自動的に検出されます。

ただし、Blade コンポーネントを利用するパッケージを構築している場合は、コンポーネント クラスとその HTML タグ エイリアスを手動で登録する必要があります。通常、コンポーネントはパッケージのサービスプロバイダの `boot` メソッドに登録する必要があります。

    use Illuminate\Support\Facades\Blade;

    /**
     * Bootstrap your package's services.
     */
    public function boot()
    {
        Blade::component('package-alert', Alert::class);
    }

コンポーネントが登録されると、そのタグ エイリアスを使用してレンダリングできます。

```blade
<x-package-alert/>
```

あるいは、`componentNamespace` メソッドを使用して、規則に従ってコンポーネント クラスを自動ロードすることもできます。たとえば、`Nightshade` パッケージには、`Package\Views\Components` 名前空間内に存在する `Calendar` コンポーネントと `ColorPicker` コンポーネントが含まれる場合があります。

    use Illuminate\Support\Facades\Blade;

    /**
     * Bootstrap your package's services.
     *
     * @return void
     */
    public function boot()
    {
        Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
    }

これにより、`package-name::` 構文を使用して、ベンダー名前空間によるパッケージ コンポーネントの使用が許可されます。

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade は、コンポーネント名をパスカル文字に変換することで、このコンポーネントにリンクされているクラスを自動的に検出します。サブディレクトリは、「ドット」表記を使用してサポートされています。

<a name="rendering-components"></a>
### レンダリングコンポーネント

コンポーネントを表示するには、Blade テンプレートの 1 つ内で Blade コンポーネント タグを使用できます。Blade コンポーネント タグは文字列 `x-` で始まり、その後にコンポーネント クラスのケバブ ケース名が続きます。

```blade
<x-alert/>

<x-user-profile/>
```

コンポーネント クラスが `app/View/Components` ディレクトリ内でさらに深くネストされている場合は、ディレクトリのネストを示すために `.` 文字を使用できます。たとえば、コンポーネントが `app/View/Components/Inputs/Button.php` にあると仮定すると、次のようにレンダリングできます。

```blade
<x-inputs.button/>
```

<a name="passing-data-to-components"></a>
### コンポーネントにデータを渡す

HTML 属性を使用してデータを Blade コンポーネントに渡すことができます。ハードコーディングされたプリミティブ値は、単純な HTML 属性文字列を使用してコンポーネントに渡すことができます。 PHP 式と変数は、接頭辞として `:` 文字を使用する属性を介してコンポーネントに渡す必要があります。

```blade
<x-alert type="error" :message="$message"/>
```

コンポーネントのすべてのデータ属性をそのクラス コンストラクターで定義する必要があります。コンポーネント上のすべてのパブリック プロパティは、コンポーネントのビューで自動的に利用できるようになります。コンポーネントの `render` メソッドからビューにデータを渡す必要はありません。

    <?php

    namespace App\View\Components;

    use Illuminate\View\Component;

    class Alert extends Component
    {
        /**
         * The alert type.
         *
         * @var string
         */
        public $type;

        /**
         * The alert message.
         *
         * @var string
         */
        public $message;

        /**
         * Create the component instance.
         *
         * @param  string  $type
         * @param  string  $message
         * @return void
         */
        public function __construct($type, $message)
        {
            $this->type = $type;
            $this->message = $message;
        }

        /**
         * Get the view / contents that represent the component.
         *
         * @return \Illuminate\View\View|\Closure|string
         */
        public function render()
        {
            return view('components.alert');
        }
    }

コンポーネントがレンダリングされるとき、変数を名前でエコーすることによって、コンポーネントのパブリック変数の内容を表示できます。

```blade
<div class="alert alert-{{ $type }}">
    {{ $message }}
</div>
```

<a name="casing"></a>
#### ケーシング

コンポーネントのコンストラクター引数は `camelCase` を使用して指定する必要がありますが、HTML 属性の引数名を参照する場合は `kebab-case` を使用する必要があります。たとえば、次のコンポーネント コンストラクターがあるとします。

    /**
     * Create the component instance.
     *
     * @param  string  $alertType
     * @return void
     */
    public function __construct($alertType)
    {
        $this->alertType = $alertType;
    }

`$alertType` 引数は、次のようにコンポーネントに指定できます。

```blade
<x-alert alert-type="danger" />
```

<a name="short-attribute-syntax"></a>
#### 短い属性構文

コンポーネントに属性を渡すときは、「短い属性」構文を使用することもできます。属性名は、対応する変数名と一致することが多いため、これは便利なことがよくあります。

```blade
{{-- Short attribute syntax... --}}
<x-profile :$userId :$name />

{{-- Is equivalent to... --}}
<x-profile :user-id="$userId" :name="$name" />
```

<a name="escaping-attribute-rendering"></a>
#### 属性レンダリングのエスケープ

Alpine.js などの一部の JavaScript フレームワークもコロン接頭辞付きの属性を使用するため、二重コロン (`::`) 接頭辞を使用して属性が PHP 式ではないことを Blade に通知できます。たとえば、次のコンポーネントがあるとします。

```blade
<x-button ::class="{ danger: isDeleting }">
    Submit
</x-button>
```

次の HTML が Blade によってレンダリングされます。

```blade
<button :class="{ danger: isDeleting }">
    Submit
</button>
```

<a name="component-methods"></a>
#### コンポーネントメソッド

コンポーネント テンプレートで使用できるパブリック変数に加えて、コンポーネント上の任意のパブリック メソッドを呼び出すことができます。たとえば、`isSelected` メソッドを持つコンポーネントを想像してください。

    /**
     * Determine if the given option is the currently selected option.
     *
     * @param  string  $option
     * @return bool
     */
    public function isSelected($option)
    {
        return $option === $this->selected;
    }

メソッドの名前に一致する変数を呼び出すことで、コンポーネント テンプレートからこのメソッドを実行できます。

```blade
<option {{ $isSelected($value) ? 'selected' : '' }} value="{{ $value }}">
    {{ $label }}
</option>
```

<a name="using-attributes-slots-within-component-class"></a>
#### コンポーネントクラス内の属性とスロットへのアクセス

Blade コンポーネントを使用すると、クラスの render メソッド内のコンポーネント名、属性、スロットにアクセスすることもできます。ただし、このデータにアクセスするには、コンポーネントの `render` メソッドからクロージャを返す必要があります。クロージャは、唯一の引数として `$data` 配列を受け取ります。この配列には、コンポーネントに関する情報を提供するいくつかの要素が含まれます。

    /**
     * Get the view / contents that represent the component.
     *
     * @return \Illuminate\View\View|\Closure|string
     */
    public function render()
    {
        return function (array $data) {
            // $data['componentName'];
            // $data['attributes'];
            // $data['slot'];

            return '<div>Components content</div>';
        };
    }

`componentName` は、HTML タグで `x-` プレフィックスの後に使用される名前と同じです。したがって、`<x-alert />` の `componentName` は `alert` になります。 `attributes` 要素には、HTML タグに存在したすべての属性が含まれます。 `slot` 要素は、コンポーネントのスロットの内容を含む `Illuminate\Support\HtmlString` インスタンスです。

クロージャは文字列を返す必要があります。返された文字列が既存のビューに対応する場合、そのビューがレンダリングされます。それ以外の場合、返された文字列はインライン Blade ビューとして評価されます。

<a name="additional-dependencies"></a>
#### 追加の依存関係

コンポーネントが Laravel の [サービスコンテナ](/docs/{{version}}/container) からの依存関係を必要とする場合、コンポーネントのデータ属性の前に依存関係をリストすると、それらはコンテナーによって自動的に挿入されます。

```php
use App\Services\AlertCreator;

/**
 * Create the component instance.
 *
 * @param  \App\Services\AlertCreator  $creator
 * @param  string  $type
 * @param  string  $message
 * @return void
 */
public function __construct(AlertCreator $creator, $type, $message)
{
    $this->creator = $creator;
    $this->type = $type;
    $this->message = $message;
}
```

<a name="hiding-attributes-and-methods"></a>
#### 属性/メソッドの非表示

一部のパブリック メソッドまたはプロパティが変数としてコンポーネント テンプレートに公開されるのを防ぎたい場合は、それらをコンポーネントの `$except` 配列プロパティに追加できます。

    <?php

    namespace App\View\Components;

    use Illuminate\View\Component;

    class Alert extends Component
    {
        /**
         * The alert type.
         *
         * @var string
         */
        public $type;

        /**
         * The properties / methods that should not be exposed to the component template.
         *
         * @var array
         */
        protected $except = ['type'];
    }

<a name="component-attributes"></a>
### コンポーネントの属性

データ属性をコンポーネントに渡す方法はすでに検討しました。ただし、コンポーネントが機能するために必要なデータの一部ではない、`class` などの追加の HTML 属性を指定する必要がある場合があります。通常、これらの追加属性はコンポーネント テンプレートのルート要素に渡します。たとえば、次のように `alert` コンポーネントをレンダリングしたいとします。

```blade
<x-alert type="error" :message="$message" class="mt-4"/>
```

コンポーネントのコンストラクターの一部ではないすべての属性は、コンポーネントの「属性バッグ」に自動的に追加されます。この属性バッグは、`$attributes` 変数を介してコンポーネントで自動的に使用できるようになります。この変数をエコーすることで、すべての属性をコンポーネント内でレンダリングできます。

```blade
<div {{ $attributes }}>
    <!-- Component content -->
</div>
```

> **警告**
> 現時点では、コンポーネント タグ内での `@env` などのディレクティブの使用はサポートされていません。たとえば、`<x-alert :live="@env('production')"/>` はコンパイルされません。

<a name="default-merged-attributes"></a>
#### デフォルト/結合された属性

場合によっては、属性のデフォルト値を指定したり、コンポーネントの属性の一部に追加の値をマージしたりすることが必要な場合があります。これを実現するには、属性バッグの `merge` メソッドを使用できます。このメソッドは、コンポーネントに常に適用する必要がある一連のデフォルト CSS クラスを定義する場合に特に役立ちます。

```blade
<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

このコンポーネントが次のように利用されると仮定すると、次のようになります。

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

コンポーネントの最終的にレンダリングされた HTML は次のように表示されます。

```blade
<div class="alert alert-error mb-4">
    <!-- Contents of the $message variable -->
</div>
```

<a name="conditionally-merge-classes"></a>
#### 条件付きクラスのマージ

特定の条件が `true` の場合、クラスをマージしたい場合があります。これは、`class` メソッドを使用して実行できます。このメソッドは、値がブール式の場合、配列キーに追加するクラスが含まれるクラスの配列を受け取ります。配列要素に数値キーがある場合、その要素は常に表示されるクラス リストに含まれます。

```blade
<div {{ $attributes->class(['p-4', 'bg-red' => $hasError]) }}>
    {{ $message }}
</div>
```

他の属性をコンポーネントにマージする必要がある場合は、`merge` メソッドを `class` メソッドにチェーンできます。

```blade
<button {{ $attributes->class(['p-4'])->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

> **注記**
> マージされた属性を受け取るべきではない他の HTML 要素のクラスを条件付きでコンパイルする必要がある場合は、[`@class` ディレクティブ](#conditional-classes) を使用できます。

<a name="non-class-attribute-merging"></a>
#### 非クラス属性の結合

`class` 属性ではない属性をマージする場合、`merge` メソッドに指定された値は属性の「デフォルト」値とみなされます。ただし、`class` 属性とは異なり、これらの属性は挿入された属性値とマージされません。代わりに、上書きされます。たとえば、`button` コンポーネントの実装は次のようになります。

```blade
<button {{ $attributes->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

カスタム `type` を使用してボタン コンポーネントをレンダリングするには、コンポーネントを使用するときに指定できます。タイプが指定されていない場合は、`button` タイプが使用されます。

```blade
<x-button type="submit">
    Submit
</x-button>
```

この例の `button` コンポーネントのレンダリングされた HTML は次のようになります。

```blade
<button type="submit">
    Submit
</button>
```

`class` 以外の属性のデフォルト値と挿入された値を結合したい場合は、`prepends` メソッドを使用できます。この例では、`data-controller` 属性は常に `profile-controller` で始まり、追加で挿入された `data-controller` 値はこのデフォルト値の後に配置されます。

```blade
<div {{ $attributes->merge(['data-controller' => $attributes->prepends('profile-controller')]) }}>
    {{ $slot }}
</div>
```

<a name="filtering-attributes"></a>
#### 属性の取得とフィルタリング

`filter` メソッドを使用して属性をフィルタリングできます。このメソッドは、属性バッグに属性を保持したい場合に `true` を返すクロージャを受け入れます。

```blade
{{ $attributes->filter(fn ($value, $key) => $key == 'foo') }}
```

便宜上、`whereStartsWith` メソッドを使用して、キーが指定された文字列で始まるすべての属性を取得できます。

```blade
{{ $attributes->whereStartsWith('wire:model') }}
```

逆に、`whereDoesntStartWith` メソッドを使用して、キーが指定された文字列で始まるすべての属性を除外することもできます。

```blade
{{ $attributes->whereDoesntStartWith('wire:model') }}
```

`first` メソッドを使用すると、指定された属性バッグの最初の属性をレンダリングできます。

```blade
{{ $attributes->whereStartsWith('wire:model')->first() }}
```

コンポーネントに属性が存在するかどうかを確認したい場合は、`has` メソッドを使用できます。このメソッドは、属性名を唯一の引数として受け入れ、属性が存在するかどうかを示すブール値を返します。

```blade
@if ($attributes->has('class'))
    <div>Class attribute is present</div>
@endif
```

`get` メソッドを使用して、特定の属性の値を取得できます。

```blade
{{ $attributes->get('class') }}
```

<a name="reserved-keywords"></a>
### 予約されたキーワード

デフォルトでは、一部のキーワードはコンポーネントをレンダリングするために Blade の内部使用のために予約されています。次のキーワードは、コンポーネント内のパブリック プロパティまたはメソッド名として定義できません。

<div class="content-list" markdown="1">

- `data`
- `render`
- `resolveView`
- `shouldRender`
- `view`
- `withAttributes`
- `withName`

</div>

<a name="slots"></a>
### スロット

多くの場合、追加のコンテンツを「スロット」経由でコンポーネントに渡す必要があります。コンポーネント スロットは、`$slot` 変数をエコーすることによってレンダリングされます。この概念を詳しく調べるために、`alert` コンポーネントに次のマークアップがあると想像してみましょう。

```blade
<!-- /resources/views/components/alert.blade.php -->

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

コンポーネントにコンテンツを挿入することで、コンテンツを `slot` に渡すことができます。

```blade
<x-alert>
    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

場合によっては、コンポーネントがコンポーネント内の異なる場所に複数の異なるスロットをレンダリングする必要がある場合があります。 「タイトル」スロットを挿入できるようにアラート コンポーネントを変更しましょう。

```blade
<!-- /resources/views/components/alert.blade.php -->

<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    {{ $slot }}
</div>
```

`x-slot` タグを使用して、名前付きスロットの内容を定義できます。明示的な `x-slot` タグ内にないコンテンツは、`$slot` 変数のコンポーネントに渡されます。

```xml
<x-alert>
    <x-slot:title>
        Server Error
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```

<a name="scoped-slots"></a>
#### スコープ付きスロット

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
#### スロットの属性

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

スロット属性を操作するには、スロットの変数の `attributes` プロパティにアクセスします。属性の操作方法の詳細については、[コンポーネントの属性](#component-attributes) のドキュメントを参照してください。

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
### インラインコンポーネントビュー

非常に小さなコンポーネントの場合、コンポーネント クラスとコンポーネントのビュー テンプレートの両方を管理するのが面倒に感じる場合があります。このため、コンポーネントのマークアップを `render` メソッドから直接返すことができます。

    /**
     * Get the view / contents that represent the component.
     *
     * @return \Illuminate\View\View|\Closure|string
     */
    public function render()
    {
        return <<<'blade'
            <div class="alert alert-danger">
                {{ $slot }}
            </div>
        blade;
    }

<a name="generating-inline-view-components"></a>
#### インラインビューコンポーネントの生成

インライン ビューをレンダリングするコンポーネントを作成するには、`make:component` コマンドの実行時に `inline` オプションを使用できます。

```shell
php artisan make:component Alert --inline
```

<a name="dynamic-components"></a>
### 動的コンポーネント

コンポーネントをレンダリングする必要があるが、実行時までどのコンポーネントをレンダリングすべきかわからない場合があります。この状況では、Laravel の組み込み `dynamic-component` コンポーネントを使用して、実行時の値または変数に基づいてコンポーネントをレンダリングできます。

```blade
<x-dynamic-component :component="$componentName" class="mt-4" />
```

<a name="manually-registering-components"></a>
### コンポーネントを手動で登録する

> **警告**
> コンポーネントの手動登録に関する次のドキュメントは、主にビューコンポーネントを含む Laravel パッケージを作成する人に適用されます。パッケージを作成していない場合、コンポーネントのドキュメントのこの部分は関係ない可能性があります。

独自のアプリケーションのコンポーネントを作成する場合、コンポーネントは `app/View/Components` ディレクトリおよび `resources/views/components` ディレクトリ内で自動的に検出されます。

ただし、Blade コンポーネントを利用するパッケージを構築する場合、またはコンポーネントを従来とは異なるディレクトリに配置する場合は、Laravel がコンポーネントの場所を認識できるように、コンポーネント クラスとその HTML タグのエイリアスを手動で登録する必要があります。通常、コンポーネントはパッケージのサービスプロバイダの `boot` メソッドに登録する必要があります。

    use Illuminate\Support\Facades\Blade;
    use VendorPackage\View\Components\AlertComponent;

    /**
     * Bootstrap your package's services.
     *
     * @return void
     */
    public function boot()
    {
        Blade::component('package-alert', AlertComponent::class);
    }

コンポーネントが登録されると、そのタグ エイリアスを使用してレンダリングできます。

```blade
<x-package-alert/>
```

#### パッケージコンポーネントの自動ロード

あるいは、`componentNamespace` メソッドを使用して、規則に従ってコンポーネント クラスを自動ロードすることもできます。たとえば、`Nightshade` パッケージには、`Package\Views\Components` 名前空間内に存在する `Calendar` コンポーネントと `ColorPicker` コンポーネントが含まれる場合があります。

    use Illuminate\Support\Facades\Blade;

    /**
     * Bootstrap your package's services.
     *
     * @return void
     */
    public function boot()
    {
        Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
    }

これにより、`package-name::` 構文を使用して、ベンダー名前空間によるパッケージ コンポーネントの使用が許可されます。

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```

Blade は、コンポーネント名をパスカル文字に変換することで、このコンポーネントにリンクされているクラスを自動的に検出します。サブディレクトリは、「ドット」表記を使用してサポートされています。

<a name="anonymous-components"></a>
## 匿名コンポーネント (Anonymous Components)

インライン コンポーネントと同様に、匿名コンポーネントは、単一のファイルを介してコンポーネントを管理するメカニズムを提供します。ただし、匿名コンポーネントは単一のビュー ファイルを使用し、関連するクラスを持ちません。匿名コンポーネントを定義するには、`resources/views/components` ディレクトリ内に Blade テンプレートを配置するだけです。たとえば、`resources/views/components/alert.blade.php` でコンポーネントを定義したと仮定すると、次のように単純にレンダリングできます。

```blade
<x-alert/>
```

`.` 文字を使用して、コンポーネントが `components` ディレクトリのさらに深くネストされているかどうかを示すことができます。たとえば、コンポーネントが `resources/views/components/inputs/button.blade.php` で定義されていると仮定すると、次のようにレンダリングできます。

```blade
<x-inputs.button/>
```

<a name="anonymous-index-components"></a>
### 匿名インデックスコンポーネント

コンポーネントが多数の Blade テンプレートで構成されている場合、特定のコンポーネントのテンプレートを 1 つのディレクトリ内にグループ化したい場合があります。たとえば、次のディレクトリ構造を持つ「accordion」コンポーネントを想像してください。

```none
/resources/views/components/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```

このディレクトリ構造により、アコーディオン コンポーネントとその項目を次のようにレンダリングできます。

```blade
<x-accordion>
    <x-accordion.item>
        ...
    </x-accordion.item>
</x-accordion>
```

ただし、`x-accordion` 経由でアコーディオン コンポーネントをレンダリングするには、「インデックス」アコーディオン コンポーネント テンプレートを、他のアコーディオン関連テンプレートとともに `accordion` ディレクトリ内にネストするのではなく、`resources/views/components` ディレクトリに配置する必要がありました。

ありがたいことに、Blade では、コンポーネントのテンプレート ディレクトリ内に `index.blade.php` ファイルを配置できます。コンポーネントに `index.blade.php` テンプレートが存在する場合、それはコンポーネントの「ルート」ノードとしてレンダリングされます。したがって、上記の例で示した同じ Blade 構文を引き続き使用できます。ただし、ディレクトリ構造は次のように調整します。

```none
/resources/views/components/accordion/index.blade.php
/resources/views/components/accordion/item.blade.php
```

<a name="data-properties-attributes"></a>
### データのプロパティ/属性

匿名コンポーネントには関連付けられたクラスがないため、どのデータを変数としてコンポーネントに渡す必要があるのか​​、またどの属性をコンポーネントの [属性バッグ](#component-attributes) に配置する必要があるのか​​をどのように区別すればよいのか疑問に思うかもしれません。

コンポーネントの Blade テンプレートの先頭にある `@props` ディレクティブを使用して、どの属性をデータ変数と見なすかを指定できます。コンポーネントの他のすべての属性は、コンポーネントの属性バッグを介して利用可能になります。データ変数にデフォルト値を与えたい場合は、変数の名前を配列キーとして指定し、デフォルト値を配列値として指定できます。

```blade
<!-- /resources/views/components/alert.blade.php -->

@props(['type' => 'info', 'message'])

<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```

上記のコンポーネント定義を考慮すると、次のようにコンポーネントをレンダリングできます。

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```

<a name="accessing-parent-data"></a>
### 親データへのアクセス

場合によっては、子コンポーネント内の親コンポーネントからデータにアクセスしたい場合があります。このような場合、`@aware` ディレクティブを使用できます。たとえば、親 `<x-menu>` と子 `<x-menu.item>` で構成される複雑なメニュー コンポーネントを構築していると想像してください。

```blade
<x-menu color="purple">
    <x-menu.item>...</x-menu.item>
    <x-menu.item>...</x-menu.item>
</x-menu>
```

`<x-menu>` コンポーネントには、次のような実装が含まれる場合があります。

```blade
<!-- /resources/views/components/menu/index.blade.php -->

@props(['color' => 'gray'])

<ul {{ $attributes->merge(['class' => 'bg-'.$color.'-200']) }}>
    {{ $slot }}
</ul>
```

`color` プロパティは親 (`<x-menu>`) にのみ渡されたため、`<x-menu.item>` 内では使用できません。ただし、`@aware` ディレクティブを使用すると、`<x-menu.item>` 内でも使用できるようになります。

```blade
<!-- /resources/views/components/menu/item.blade.php -->

@aware(['color' => 'gray'])

<li {{ $attributes->merge(['class' => 'text-'.$color.'-800']) }}>
    {{ $slot }}
</li>
```

> **警告**
> `@aware` ディレクティブは、HTML 属性を介して親コンポーネントに明示的に渡されていない親データにはアクセスできません。親コンポーネントに明示的に渡されないデフォルトの `@props` 値には、`@aware` ディレクティブではアクセスできません。

<a name="anonymous-component-paths"></a>
### 匿名コンポーネントのパス

前述したように、匿名コンポーネントは通常、`resources/views/components` ディレクトリ内に Blade テンプレートを配置することによって定義されます。ただし、デフォルトのパスに加えて、他の匿名コンポーネントのパスを Laravel に登録したい場合もあります。

`anonymousComponentPath` メソッドは、匿名コンポーネントの場所への「パス」を最初の引数として受け入れ、コンポーネントを配置する必要があるオプションの「名前空間」を 2 番目の引数として受け入れます。通常、このメソッドは、アプリケーションの [サービスプロバイダ](/docs/{{version}}/providers) の 1 つの `boot` メソッドから呼び出す必要があります。

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        Blade::anonymousComponentPath(__DIR__.'/../components');
    }

上記の例のように、コンポーネント パスがプレフィックスを指定せずに登録されている場合、Blade コンポーネントでも対応するプレフィックスなしでレンダリングされる可能性があります。たとえば、上記で登録したパスに `panel.blade.php` コンポーネントが存在する場合、次のようにレンダリングされます。

```blade
<x-panel />
```

プレフィックス「namespaces」は、`anonymousComponentPath` メソッドの 2 番目の引数として指定できます。

    Blade::anonymousComponentPath(__DIR__.'/../components', 'dashboard');

プレフィックスが指定されている場合、コンポーネントがレンダリングされるときに、コンポーネントの名前空間にコンポーネント名をプレフィックスとして付けることによって、その「名前空間」内のコンポーネントがレンダリングされることがあります。

```blade
<x-dashboard::panel />
```

<a name="building-layouts"></a>
## 建物のレイアウト (Building Layouts)

<a name="layouts-using-components"></a>
### コンポーネントを使用したレイアウト

ほとんどの Web アプリケーションは、さまざまなページにわたって同じ一般的なレイアウトを維持します。作成するすべてのビューでレイアウト HTML 全体を繰り返す必要がある場合、アプリケーションを保守するのは非常に面倒で困難になります。ありがたいことに、このレイアウトを単一の [Blade コンポーネント](#components) として定義し、アプリケーション全体で使用すると便利です。

<a name="defining-the-layout-component"></a>
#### レイアウトコンポーネントの定義

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
#### レイアウトコンポーネントの適用

`layout` コンポーネントが定義されたら、そのコンポーネントを利用するBlade ビューを作成できます。この例では、タスク リストを表示する単純なビューを定義します。

```blade
<!-- resources/views/tasks.blade.php -->

<x-layout>
    @foreach ($tasks as $task)
        {{ $task }}
    @endforeach
</x-layout>
```

コンポーネントに挿入されるコンテンツは、`layout` コンポーネント内のデフォルトの `$slot` 変数に提供されることに注意してください。お気づきかもしれませんが、`layout` は、`$title` スロットが提供されている場合はそれも尊重します。それ以外の場合は、デフォルトのタイトルが表示されます。 [コンポーネントのドキュメント](#components) で説明されている標準スロット構文を使用して、タスク リスト ビューからカスタム タイトルを挿入できます。

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

レイアウト ビューとタスク リスト ビューを定義したので、あとはルートから `task` ビューを返すだけです。

    use App\Models\Task;

    Route::get('/tasks', function () {
        return view('tasks', ['tasks' => Task::all()]);
    });

<a name="layouts-using-template-inheritance"></a>
### テンプレートの継承を使用したレイアウト

<a name="defining-a-layout"></a>
#### レイアウトの定義

レイアウトは「テンプレートの継承」によって作成することもできます。これは、[components](#components) が導入される前は、アプリケーションを構築する主な方法でした。

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

ご覧のとおり、このファイルには典型的な HTML マークアップが含まれています。ただし、`@section` ディレクティブと `@yield` ディレクティブに注意してください。 `@section` ディレクティブは、名前が示すとおり、コンテンツのセクションを定義します。一方、`@yield` ディレクティブは、特定のセクションのコンテンツを表示するために使用されます。

アプリケーションのレイアウトを定義したので、そのレイアウトを継承する子ページを定義しましょう。

<a name="extending-a-layout"></a>
#### レイアウトの拡張

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

この例では、`sidebar` セクションは `@@parent` ディレクティブを利用して、レイアウトのサイドバーにコンテンツを (上書きではなく) 追加しています。 `@@parent` ディレクティブは、ビューがレンダリングされるときにレイアウトのコンテンツに置き換えられます。

> **注記**
> 前の例とは異なり、この `sidebar` セクションは、`@show` ではなく `@endsection` で終わります。 `@endsection` ディレクティブはセクションを定義するだけですが、`@show` はセクションを定義して **即座に生成**します。

`@yield` ディレクティブは、2 番目のパラメーターとしてデフォルト値も受け入れます。この値は、生成されるセクションが未定義の場合に表示されます。

```blade
@yield('content', 'Default content')
```

<a name="forms"></a>
## フォーム (Forms)

<a name="csrf-field"></a>
### CSRFフィールド

アプリケーションで HTML フォームを定義するときは常に、[CSRF保護](/docs/{{version}}/csrf) ミドルウェアがリクエストを検証できるように、フォームに非表示の CSRF トークン フィールドを含める必要があります。 `@csrf` Blade ディレクティブを使用してトークン フィールドを生成できます。

```blade
<form method="POST" action="/profile">
    @csrf

    ...
</form>
```

<a name="method-field"></a>
### メソッドフィールド

HTML フォームは `PUT`、`PATCH`、または `DELETE` リクエストを作成できないため、これらの HTTP 動詞を偽装するには、非表示の `_method` フィールドを追加する必要があります。 `@method` Blade ディレクティブは、このフィールドを作成できます。

```blade
<form action="/foo/bar" method="POST">
    @method('PUT')

    ...
</form>
```

<a name="validation-errors"></a>
### 検証エラー

`@error` ディレクティブを使用すると、特定の属性に [検証エラーメッセージ](/docs/{{version}}/validation#quick-displaying-the-validation-errors) が存在するかどうかをすばやく確認できます。 `@error` ディレクティブ内で、`$message` 変数をエコーし​​てエラー メッセージを表示できます。

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

`@error` ディレクティブは「if」ステートメントにコンパイルされるため、属性にエラーがない場合は、`@else` ディレクティブを使用してコンテンツをレンダリングできます。

```blade
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input id="email"
    type="email"
    class="@error('email') is-invalid @else is-valid @enderror">
```

[特定のエラーバッグの名前](/docs/{{version}}/validation#named-error-bags) を `@error` ディレクティブの 2 番目のパラメーターとして渡して、複数のフォームを含むページの検証エラー メッセージを取得できます。

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
## スタック (Stacks)

Blade を使用すると、別のビューまたはレイアウトの別の場所にレンダリングできる名前付きスタックにプッシュできます。これは、子ビューで必要な JavaScript ライブラリを指定する場合に特に役立ちます。

```blade
@push('scripts')
    <script src="/example.js"></script>
@endpush
```

指定されたブール式が `true` と評価された場合に `@push` コンテンツを取得したい場合は、`@pushIf` ディレクティブを使用できます。

```blade
@pushIf($shouldPush, 'scripts')
    <script src="/example.js"></script>
@endPushIf
```

必要に応じて何度でもスタックにプッシュできます。完全なスタックの内容をレンダリングするには、スタックの名前を `@stack` ディレクティブに渡します。

```blade
<head>
    <!-- Head Contents -->

    @stack('scripts')
</head>
```

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
## サービスインジェクション (Service Injection)

`@inject` ディレクティブは、Laravel [サービスコンテナ](/docs/{{version}}/container) からサービスを取得するために使用できます。 `@inject` に渡される最初の引数はサービスが配置される変数の名前であり、2 番目の引数は解決するサービスのクラス名またはインターフェイス名です。

```blade
@inject('metrics', 'App\Services\MetricsService')

<div>
    Monthly Revenue: {{ $metrics->monthlyRevenue() }}.
</div>
```

<a name="rendering-inline-blade-templates"></a>
## インラインBlade テンプレートのレンダリング (Rendering Inline Blade Templates)

場合によっては、生の Blade テンプレート文字列を有効な HTML に変換する必要があるかもしれません。これは、`Blade` ファサードによって提供される `render` メソッドを使用して実行できます。 `render` メソッドは、Blade テンプレート文字列と、テンプレートに提供するオプションのデータ配列を受け入れます。

```php
use Illuminate\Support\Facades\Blade;

return Blade::render('Hello, {{ $name }}', ['name' => 'Julian Bashir']);
```

Laravel は、インライン Blade テンプレートを `storage/framework/views` ディレクトリに書き込むことでレンダリングします。 Blade テンプレートのレンダリング後に Laravel にこれらの一時ファイルを削除させたい場合は、メソッドに `deleteCachedView` 引数を指定できます。

```php
return Blade::render(
    'Hello, {{ $name }}',
    ['name' => 'Julian Bashir'],
    deleteCachedView: true
);
```

<a name="rendering-blade-fragments"></a>
## 刃の破片のレンダリング (Rendering Blade Fragments)

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

次に、このテンプレートを利用するビューをレンダリングするときに、`fragment` メソッドを呼び出して、指定されたフラグメントのみが送信 HTTP 応答に含まれるように指定できます。

```php
return view('dashboard', ['users' => $users])->fragment('user-list');
```

`fragmentIf` メソッドを使用すると、指定された条件に基づいてビューのフラグメントを条件付きで返すことができます。それ以外の場合は、ビュー全体が返されます。

```php
return view('dashboard', ['users' => $users])
    ->fragmentIf($request->hasHeader('HX-Request'), 'user-list');
```

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
## 伸びる刃 (Extending Blade)

Blade では、`directive` メソッドを使用して独自のカスタム ディレクティブを定義できます。 Blade コンパイラはカスタム ディレクティブを検出すると、ディレクティブに含まれる式を使用して提供されたコールバックを呼び出します。

次の例では、指定された `$var` をフォーマットする `@datetime($var)` ディレクティブを作成します。これは、`DateTime` のインスタンスである必要があります。

    <?php

    namespace App\Providers;

    use Illuminate\Support\Facades\Blade;
    use Illuminate\Support\ServiceProvider;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * Register any application services.
         *
         * @return void
         */
        public function register()
        {
            //
        }

        /**
         * Bootstrap any application services.
         *
         * @return void
         */
        public function boot()
        {
            Blade::directive('datetime', function ($expression) {
                return "<?php echo ($expression)->format('m/d/Y H:i'); ?>";
            });
        }
    }

ご覧のとおり、ディレクティブに渡される式に `format` メソッドを連鎖させます。したがって、この例では、このディレクティブによって生成される最終的な PHP は次のようになります。

    <?php echo ($var)->format('m/d/Y H:i'); ?>

> **警告**
> Blade ディレクティブのロジックを更新した後、キャッシュされた Blade ビューをすべて削除する必要があります。キャッシュされたBlade ビューは、`view:clear` Artisan コマンドを使用して削除できます。

<a name="custom-echo-handlers"></a>
### カスタム エコー ハンドラー

Blade を使用してオブジェクトを「エコー」しようとすると、オブジェクトの `__toString` メソッドが呼び出されます。 [`__toString`](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) メソッドは、PHP の組み込み「マジック メソッド」の 1 つです。ただし、対話しているクラスがサードパーティのライブラリに属している場合など、特定のクラスの `__toString` メソッドを制御できない場合があります。

このような場合、Blade では、その特定の種類のオブジェクトにカスタム エコー ハンドラーを登録できます。これを実現するには、Blade の `stringable` メソッドを呼び出す必要があります。 `stringable` メソッドはクロージャを受け入れます。このクロージャは、レンダリングを担当するオブジェクトのタイプをタイプヒントする必要があります。通常、`stringable` メソッドは、アプリケーションの `AppServiceProvider` クラスの `boot` メソッド内で呼び出す必要があります。

    use Illuminate\Support\Facades\Blade;
    use Money\Money;

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        Blade::stringable(function (Money $money) {
            return $money->formatTo('en_GB');
        });
    }

カスタム エコー ハンドラーを定義したら、Blade テンプレート内のオブジェクトをエコーするだけです。

```blade
Cost: {{ $money }}
```

<a name="custom-if-statements"></a>
### カスタムの If ステートメント

カスタム ディレクティブのプログラミングは、単純なカスタム条件文を定義する場合、必要以上に複雑になる場合があります。そのため、Blade は、クロージャを使用してカスタム条件ディレクティブを迅速に定義できる `Blade::if` メソッドを提供します。たとえば、アプリケーションに設定されたデフォルトの「ディスク」をチェックするカスタム条件を定義してみましょう。これは、`AppServiceProvider` の `boot` メソッドで行うことができます。

    use Illuminate\Support\Facades\Blade;

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        Blade::if('disk', function ($value) {
            return config('filesystems.default') === $value;
        });
    }

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

