<!-- # Release Notes -->
# Release Notes

- [Versioning Scheme](#versioning-scheme)
- [Support Policy](#support-policy)
- [Laravel 10](#laravel-10)

<a name="versioning-scheme"></a>
<!-- ## Versioning Scheme -->
## Versioning Scheme

<!-- Laravel and its other first-party packages follow [Semantic Versioning](https://semver.org). Major framework releases are released every year (~Q1), while minor and patch releases may be released as often as every week. Minor and patch releases should **never** contain breaking changes. -->
Laravel とその他のファーストパーティ パッケージは [Semantic Versioning](https://semver.org) に従います。メジャー フレームワーク リリースは毎年 (~第 1 四半期) リリースされますが、マイナー リリースとパッチ リリースは毎週リリースされる場合があります。マイナー リリースとパッチ リリースには重大な変更が含まれてはなりません**。

<!-- When referencing the Laravel framework or its components from your application or package, you should always use a version constraint such as `^10.0`, since major releases of Laravel do include breaking changes. However, we strive to always ensure you may update to a new major release in one day or less. -->
Laravel のメジャーリリースには重大な変更が含まれるため、アプリケーションまたはパッケージから Laravel フレームワークまたはそのコンポーネントを参照する場合は、必ず `^10.0` などのバージョン制約を使用する必要があります。ただし、私たちは常に 1 日以内に新しいメジャー リリースに更新できるように努めています。

<a name="named-arguments"></a>
<!-- #### Named Arguments -->
#### Named Arguments

<!-- [Named arguments](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments) are not covered by Laravel's backwards compatibility guidelines. We may choose to rename function arguments when necessary in order to improve the Laravel codebase. Therefore, using named arguments when calling Laravel methods should be done cautiously and with the understanding that the parameter names may change in the future. -->
[Named arguments](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments) は、Laravel の下位互換性ガイドラインではカバーされていません。 Laravel コードベースを改善するために、必要に応じて関数の引数の名前を変更することもできます。したがって、Laravelメソッドを呼び出すときに名前付き引数を使用する場合は、パラメータ名が将来変更される可能性があることを理解した上で、慎重に行う必要があります。

<a name="support-policy"></a>
<!-- ## Support Policy -->
## Support Policy

<!-- For all Laravel releases, bug fixes are provided for 18 months and security fixes are provided for 2 years. For all additional libraries, including Lumen, only the latest major release receives bug fixes. In addition, please review the database versions [supported by Laravel](/docs/10.x/database#introduction). -->
すべての Laravel リリースでは、バグ修正は 18 か月間提供され、セキュリティ修正は 2 年間提供されます。 Lumen を含むすべての追加ライブラリについては、最新のメジャー リリースのみがバグ修正を受けます。さらに、データベースのバージョン [supported by Laravel](/docs/10.x/database#introduction) を確認してください。


<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| バージョン | PHP(*) | リリース | バグ修正まで | セキュリティ修正の期限 |
| --- | --- | --- | --- | --- |
| 8 | 7.3 - 8.1 | 2020年9月8日 | 2022 年 7 月 26 日 | 2023 年 1 月 24 日 |
| 9 | 8.0～8.2 | 2022 年 2 月 8 日 | 2023 年 8 月 8 日 | 2024 年 2 月 6 日 |
| 10 | 8.1～8.3 | 2023 年 2 月 14 日 | 2024 年 8 月 6 日 | 2025 年 2 月 4 日 |
| 11 | 8.2～8.4 | 2024 年 3 月 12 日 | 2025 年 9 月 3 日 | 2026 年 3 月 12 日 |

<!-- </div> -->
</div>

<!--
<div class="version-colors">
    <div class="end-of-life">
        <div class="color-box"></div>
        <div>End of life</div>
    </div>
    <div class="security-fixes">
        <div class="color-box"></div>
        <div>Security fixes only</div>
    </div>
</div>
-->
<div class="version-colors">
    <div class="end-of-life">
        <div class="color-box"></div>
        <div>End of life</div>
    </div>
    <div class="security-fixes">
        <div class="color-box"></div>
        <div>Security fixes only</div>
    </div>
</div>

<!-- (*) Supported PHP versions -->
(*) サポートされている PHP バージョン

<a name="laravel-10"></a>
<!-- ## Laravel 10 -->
## Laravel 10

<!-- As you may know, Laravel transitioned to yearly releases with the release of Laravel 8. Previously, major versions were released every 6 months. This transition is intended to ease the maintenance burden on the community and challenge our development team to ship amazing, powerful new features without introducing breaking changes. Therefore, we have shipped a variety of robust features to Laravel 9 without breaking backwards compatibility. -->
ご存知かもしれませんが、Laravel 8 のリリースにより、Laravel は年次リリースに移行しました。以前は、メジャー バージョンは 6 か月ごとにリリースされていました。この移行は、コミュニティのメンテナンスの負担を軽減し、開発チームが重大な変更を導入することなく、驚くべき強力な新機能をリリースできるようにすることを目的としています。そのため、下位互換性を損なうことなく、さまざまな堅牢な機能を Laravel 9 に出荷しました。

<!-- Therefore, this commitment to ship great new features during the current release will likely lead to future "major" releases being primarily used for "maintenance" tasks such as upgrading upstream dependencies, which can be seen in these release notes. -->
したがって、現在のリリース中に優れた新機能をリリースするというこの取り組みにより、将来の「メジャー」リリースは主に上流の依存関係のアップグレードなどの「メンテナンス」タスクに使用されることになる可能性が高く、これはこれらのリリース ノートで確認できます。

<!-- Laravel 10 continues the improvements made in Laravel 9.x by introducing argument and return types to all application skeleton methods, as well as all stub files used to generate classes throughout the framework. In addition, a new, developer-friendly abstraction layer has been introduced for starting and interacting with external processes. Further, Laravel Pennant has been introduced to provide a wonderful approach to managing your application's "feature flags". -->
Laravel 10は、フレームワーク全体でクラスを生成するために使用されるすべてのスタブファイルだけでなく、アプリケーションのすべてのスケルトンメソッドに引数と戻り値の型を導入することにより、Laravel 9.xで行われた改良を継続しています。さらに、外部プロセスの開始と対話のために、開発者にとって使いやすい新しい抽象化レイヤーが導入されました。さらに、アプリケーションの「機能フラグ」を管理するための素晴らしいアプローチを提供するために、Laravel Pennant が導入されました。

<a name="php-8"></a>
<!-- ### PHP 8.1 -->
### PHP 8.1

<!-- Laravel 10.x requires a minimum PHP version of 8.1. -->
Laravel 10.x には、最小 PHP バージョン 8.1 が必要です。

<a name="types"></a>
<!-- ### Types -->
### Types

<!-- _Application skeleton and stub type-hints were contributed by [Nuno Maduro](https://github.com/nunomaduro)_. -->
_アプリケーションのスケルトンとスタブのタイプ ヒントは、[Nuno Maduro](https://github.com/nunomaduro)_ によって提供されました。

<!-- On its initial release, Laravel utilized all of the type-hinting features available in PHP at the time. However, many new features have been added to PHP in the subsequent years, including additional primitive type-hints, return types, and union types. -->
Laravel は、最初のリリースで、当時 PHP で利用可能なすべてのタイプヒント機能を利用していました。ただし、その後数年間で、追加のプリミティブ型ヒント、戻り型、共用体型など、多くの新機能が PHP に追加されました。

<!-- Laravel 10.x thoroughly updates the application skeleton and all stubs utilized by the framework to introduce argument and return types to all method signatures. In addition, extraneous "doc block" type-hint information has been deleted. -->
Laravel 10.x は、アプリケーションのスケルトンとフレームワークで使用されるすべてのスタブを徹底的に更新し、すべてのメソッド シグネチャに引数と戻り値の型を導入します。さらに、無関係な「doc block」タイプヒント情報が削除されました。

<!-- This change is entirely backwards compatible with existing applications. Therefore, existing applications that do not have these type-hints will continue to function normally. -->
この変更は、既存のアプリケーションと完全に下位互換性があります。したがって、これらのタイプヒントを持たない既存のアプリケーションは引き続き正常に機能します。

<a name="laravel-pennant"></a>
<!-- ### Laravel Pennant -->
### Laravel Pennant

<!-- _Laravel Pennant was developed by [Tim MacDonald](https://github.com/timacdonald)_. -->
_Laravel Pennant は [Tim MacDonald](https://github.com/timacdonald)_ によって開発されました。

<!-- A new first-party package, Laravel Pennant, has been released. Laravel Pennant offers a light-weight, streamlined approach to managing your application's feature flags. Out of the box, Pennant includes an in-memory `array` driver and a `database` driver for persistent feature storage. -->
新しいファーストパーティパッケージであるLaravel Pennantがリリースされました。 Laravel Pennant は、アプリケーションの機能フラグを管理するための軽量で合理的なアプローチを提供します。すぐに使えるPennant には、永続的な機能ストレージ用のインメモリ `array` ドライバと `database` ドライバが含まれています。

<!-- Features can be easily defined via the `Feature::define` method: -->
機能は、`Feature::define` メソッドを使用して簡単に定義できます。

```php
use Laravel\Pennant\Feature;
use Illuminate\Support\Lottery;

Feature::define('new-onboarding-flow', function () {
    return Lottery::odds(1, 10);
});
```

<!-- Once a feature has been defined, you may easily determine if the current user has access to the given feature: -->
機能を定義すると、現在のユーザーが特定の機能にアクセスできるかどうかを簡単に判断できます。

```php
if (Feature::active('new-onboarding-flow')) {
    // ...
}
```

<!-- Of course, for convenience, Blade directives are also available: -->
もちろん、便宜上、Blade ディレクティブも利用できます。

```blade
@feature('new-onboarding-flow')
    <div>
        <!-- ... -->
    </div>
@endfeature
```

<!-- Pennant offers a variety of more advanced features and APIs. For more information, please consult the [comprehensive Pennant documentation](/docs/10.x/pennant). -->
Pennant は、さまざまなより高度な機能と API を提供します。詳細については、[comprehensive Pennant documentation](/docs/10.x/pennant) を参照してください。

<a name="process"></a>
<!-- ### Process Interaction -->
### Process Interaction

<!-- _The process abstraction layer was contributed by [Nuno Maduro](https://github.com/nunomaduro) and [Taylor Otwell](https://github.com/taylorotwell)_. -->
_プロセス抽象化レイヤーは、[Nuno Maduro](https://github.com/nunomaduro) および [Taylor Otwell](https://github.com/taylorotwell)_ によって提供されました。

<!-- Laravel 10.x introduces a beautiful abstraction layer for starting and interacting with external processes via a new `Process` facade: -->
Laravel 10.x では、新しい `Process` ファサードを介して外部プロセスを開始および対話するための美しい抽象化レイヤーが導入されています。

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

return $result->output();
```

<!-- Processes may even be started in pools, allowing for the convenient execution and management of concurrent processes: -->
プロセスはプール内で開始することもできるため、同時プロセスの実行と管理が便利になります。

```php
use Illuminate\Process\Pool;
use Illuminate\Support\Facades\Process;

[$first, $second, $third] = Process::concurrently(function (Pool $pool) {
    $pool->command('cat first.txt');
    $pool->command('cat second.txt');
    $pool->command('cat third.txt');
});

return $first->output();
```

<!-- In addition, processes may be faked for convenient testing: -->
さらに、テストを便利にするためにプロセスが偽装される場合があります。

```php
Process::fake();

// ...

Process::assertRan('ls -la');
```

<!-- For more information on interacting with processes, please consult the [comprehensive process documentation](/docs/10.x/processes). -->
プロセスとの対話の詳細については、[comprehensive process documentation](/docs/10.x/processes) を参照してください。

<a name="test-profiling"></a>
<!-- ### Test Profiling -->
### Test Profiling

<!-- _Test profiling was contributed by [Nuno Maduro](https://github.com/nunomaduro)_. -->
_テスト プロファイリングは [Nuno Maduro](https://github.com/nunomaduro)_ によって提供されました。

<!-- The Artisan `test` command has received a new `--profile` option that allows you to easily identify the slowest tests in your application: -->
Artisan `test` コマンドに、アプリケーション内で最も遅いテストを簡単に特定できる新しい `--profile` オプションが追加されました。

```shell
php artisan test --profile
```

<!-- For convenience, the slowest tests will be displayed directly within the CLI output: -->
便宜上、最も遅いテストは CLI 出力内に直接表示されます。

<!--
<p align="center">
    <img width="100%" src="https://user-images.githubusercontent.com/5457236/217328439-d8d983ec-d0fc-4cde-93d9-ae5bccf5df14.png"/>
</p>
-->
<p align="center">
    <img width="100%" src="https://user-images.githubusercontent.com/5457236/217328439-d8d983ec-d0fc-4cde-93d9-ae5bccf5df14.png"/>
</p>

<a name="pest-scaffolding"></a>
<!-- ### Pest Scaffolding -->
### Pest Scaffolding

<!-- New Laravel projects may now be created with Pest test scaffolding by default. To opt-in to this feature, provide the `--pest` flag when creating a new application via the Laravel installer: -->
新しい Laravel プロジェクトは、デフォルトで Pest テスト スキャフォールディングを使用して作成できるようになりました。この機能をオプトインするには、Laravel インストーラー経由で新しいアプリケーションを作成するときに `--pest` フラグを指定します。

```shell
laravel new example-application --pest
```

<a name="generator-cli-prompts"></a>
<!-- ### Generator CLI Prompts -->
### Generator CLI Prompts

<!-- _Generator CLI prompts were contributed by [Jess Archer](https://github.com/jessarcher)_. -->
_Generator CLI プロンプトは、[Jess Archer](https://github.com/jessarcher)_ によって提供されました。

<!-- To improve the framework's developer experience, all of Laravel's built-in `make` commands no longer require any input. If the commands are invoked without input, you will be prompted for the required arguments: -->
フレームワークの開発者エクスペリエンスを向上させるために、Laravel のすべての組み込み `make` コマンドでは入力が不要になりました。入力せずにコマンドを呼び出すと、必要な引数の入力を求めるプロンプトが表示されます。

```shell
php artisan make:controller
```

<a name="horizon-telescope-facelift"></a>
<!-- ### Horizon / Telescope Facelift -->
### Horizon / Telescope Facelift

<!-- [Horizon](/docs/10.x/horizon) and [Telescope](/docs/10.x/telescope) have been updated with a fresh, modern look including improved typography, spacing, and design: -->
[Horizon](/docs/10.x/horizon) および [Telescope](/docs/10.x/telescope) は、タイポグラフィー、間隔、デザインの改善など、新鮮でモダンな外観で更新されました。

<!-- <img src="https://laravel.com/img/docs/horizon-example.png"/> -->
<img src="https://laravel.com/img/docs/horizon-example.png"/>

