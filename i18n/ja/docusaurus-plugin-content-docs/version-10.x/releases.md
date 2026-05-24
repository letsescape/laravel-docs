# リリースノート (Release Notes)

- [バージョン管理スキーム](#versioning-scheme)
- [サポートポリシー](#support-policy)
- [Laravel10](#laravel-10)

<a name="versioning-scheme"></a>
## バージョン管理スキーム (Versioning Scheme)

Laravel とその他のファーストパーティ パッケージは [セマンティック バージョニング](https://semver.org) に従います。メジャー フレームワーク リリースは毎年 (~第 1 四半期) リリースされますが、マイナー リリースとパッチ リリースは毎週リリースされる場合があります。マイナー リリースとパッチ リリースには重大な変更が含まれてはなりません**。

Laravel のメジャーリリースには重大な変更が含まれるため、アプリケーションまたはパッケージから Laravel フレームワークまたはそのコンポーネントを参照する場合は、必ず `^10.0` などのバージョン制約を使用する必要があります。ただし、私たちは常に 1 日以内に新しいメジャー リリースに更新できるように努めています。

<a name="named-arguments"></a>
#### 名前付き引数

[名前付き引数](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments) は、Laravel の下位互換性ガイドラインではカバーされていません。 Laravel コードベースを改善するために、必要に応じて関数の引数の名前を変更することもできます。したがって、Laravelメソッドを呼び出すときに名前付き引数を使用する場合は、パラメータ名が将来変更される可能性があることを理解した上で、慎重に行う必要があります。

<a name="support-policy"></a>
## サポートポリシー (Support Policy)

すべての Laravel リリースでは、バグ修正は 18 か月間提供され、セキュリティ修正は 2 年間提供されます。 Lumen を含むすべての追加ライブラリについては、最新のメジャー リリースのみがバグ修正を受けます。さらに、データベースのバージョン [Laravelによってサポートされています](/docs/{{version}}/database#introduction) を確認してください。


<div class="overflow-auto">

| バージョン | PHP(*) | リリース | バグ修正まで | セキュリティ修正の期限 |
| --- | --- | --- | --- | --- |
| 8 | 7.3 - 8.1 | 2020年9月8日 | 2022 年 7 月 26 日 | 2023 年 1 月 24 日 |
| 9 | 8.0～8.2 | 2022 年 2 月 8 日 | 2023 年 8 月 8 日 | 2024 年 2 月 6 日 |
| 10 | 8.1～8.3 | 2023 年 2 月 14 日 | 2024 年 8 月 6 日 | 2025 年 2 月 4 日 |
| 11 | 8.2～8.4 | 2024 年 3 月 12 日 | 2025 年 9 月 3 日 | 2026 年 3 月 12 日 |

</div>

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

(*) サポートされている PHP バージョン

<a name="laravel-10"></a>
## Laravel10 (Laravel 10)

ご存知かもしれませんが、Laravel 8 のリリースにより、Laravel は年次リリースに移行しました。以前は、メジャー バージョンは 6 か月ごとにリリースされていました。この移行は、コミュニティのメンテナンスの負担を軽減し、開発チームが重大な変更を導入することなく、驚くべき強力な新機能をリリースできるようにすることを目的としています。そのため、下位互換性を損なうことなく、さまざまな堅牢な機能を Laravel 9 に出荷しました。

したがって、現在のリリース中に優れた新機能をリリースするというこの取り組みにより、将来の「メジャー」リリースは主に上流の依存関係のアップグレードなどの「メンテナンス」タスクに使用されることになる可能性が高く、これはこれらのリリース ノートで確認できます。

Laravel 10は、フレームワーク全体でクラスを生成するために使用されるすべてのスタブファイルだけでなく、アプリケーションのすべてのスケルトンメソッドに引数と戻り値の型を導入することにより、Laravel 9.xで行われた改良を継続しています。さらに、外部プロセスの開始と対話のために、開発者にとって使いやすい新しい抽象化レイヤーが導入されました。さらに、アプリケーションの「機能フラグ」を管理するための素晴らしいアプローチを提供するために、Laravel Pennant が導入されました。

<a name="php-8"></a>
### PHP8.1

Laravel 10.x には、最小 PHP バージョン 8.1 が必要です。

<a name="types"></a>
### 種類

_アプリケーションのスケルトンとスタブのタイプ ヒントは、[ヌーノ・マドゥロ](https://github.com/nunomaduro)_ によって提供されました。

Laravel は、最初のリリースで、当時 PHP で利用可能なすべてのタイプヒント機能を利用していました。ただし、その後数年間で、追加のプリミティブ型ヒント、戻り型、共用体型など、多くの新機能が PHP に追加されました。

Laravel 10.x は、アプリケーションのスケルトンとフレームワークで使用されるすべてのスタブを徹底的に更新し、すべてのメソッド シグネチャに引数と戻り値の型を導入します。さらに、無関係な「doc block」タイプヒント情報が削除されました。

この変更は、既存のアプリケーションと完全に下位互換性があります。したがって、これらのタイプヒントを持たない既存のアプリケーションは引き続き正常に機能します。

<a name="laravel-pennant"></a>
### Laravel Pennant

_Laravel Pennant は [ティム・マクドナルド](https://github.com/timacdonald)_ によって開発されました。

新しいファーストパーティパッケージであるLaravel Pennantがリリースされました。 Laravel Pennant は、アプリケーションの機能フラグを管理するための軽量で合理的なアプローチを提供します。すぐに使えるPennant には、永続的な機能ストレージ用のインメモリ `array` ドライバと `database` ドライバが含まれています。

機能は、`Feature::define` メソッドを使用して簡単に定義できます。

```php
use Laravel\Pennant\Feature;
use Illuminate\Support\Lottery;

Feature::define('new-onboarding-flow', function () {
    return Lottery::odds(1, 10);
});
```

機能を定義すると、現在のユーザーが特定の機能にアクセスできるかどうかを簡単に判断できます。

```php
if (Feature::active('new-onboarding-flow')) {
    // ...
}
```

もちろん、便宜上、Blade ディレクティブも利用できます。

```blade
@feature('new-onboarding-flow')
    <div>
        <!-- ... -->
    </div>
@endfeature
```

Pennant は、さまざまなより高度な機能と API を提供します。詳細については、[包括的なPennant のドキュメント](/docs/{{version}}/pennant) を参照してください。

<a name="process"></a>
### プロセスの相互作用

_プロセス抽象化レイヤーは、[ヌーノ・マドゥロ](https://github.com/nunomaduro) および [テイラー・オトウェル](https://github.com/taylorotwell)_ によって提供されました。

Laravel 10.x では、新しい `Process` ファサードを介して外部プロセスを開始および対話するための美しい抽象化レイヤーが導入されています。

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

return $result->output();
```

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

さらに、テストを便利にするためにプロセスが偽装される場合があります。

```php
Process::fake();

// ...

Process::assertRan('ls -la');
```

プロセスとの対話の詳細については、[包括的なプロセス文書化](/docs/{{version}}/processes) を参照してください。

<a name="test-profiling"></a>
### テストプロファイリング

_テスト プロファイリングは [ヌーノ・マドゥロ](https://github.com/nunomaduro)_ によって提供されました。

Artisan `test` コマンドに、アプリケーション内で最も遅いテストを簡単に特定できる新しい `--profile` オプションが追加されました。

```shell
php artisan test --profile
```

便宜上、最も遅いテストは CLI 出力内に直接表示されます。

<p align="center">
    <img width="100%" src="https://user-images.githubusercontent.com/5457236/217328439-d8d983ec-d0fc-4cde-93d9-ae5bccf5df14.png"/>
</p>

<a name="pest-scaffolding"></a>
### 害虫足場

新しい Laravel プロジェクトは、デフォルトで Pest テスト スキャフォールディングを使用して作成できるようになりました。この機能をオプトインするには、Laravel インストーラー経由で新しいアプリケーションを作成するときに `--pest` フラグを指定します。

```shell
laravel new example-application --pest
```

<a name="generator-cli-prompts"></a>
### ジェネレータの CLI プロンプト

_Generator CLI プロンプトは、[ジェス・アーチャー](https://github.com/jessarcher)_ によって提供されました。

フレームワークの開発者エクスペリエンスを向上させるために、Laravel のすべての組み込み `make` コマンドでは入力が不要になりました。入力せずにコマンドを呼び出すと、必要な引数の入力を求めるプロンプトが表示されます。

```shell
php artisan make:controller
```

<a name="horizon-telescope-facelift"></a>
### Horizon / Telescopeのフェイスリフト

[Horizon](/docs/{{version}}/horizon) および [Telescope](/docs/{{version}}/telescope) は、タイポグラフィー、間隔、デザインの改善など、新鮮でモダンな外観で更新されました。

<img src="https://laravel.com/img/docs/horizon-example.png">

