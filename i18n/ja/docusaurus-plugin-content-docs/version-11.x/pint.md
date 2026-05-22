# LaravelPint (Laravel Pint)

- [Introduction](#introduction)
- [Installation](#installation)
- [ランニングPint](#running-pint)
- [Pint の構成](#configuring-pint)
    - [Presets](#presets)
    - [Rules](#rules)
    - [ファイル/フォルダーの除外](#excluding-files-or-folders)
- [継続的インテグレーション](#continuous-integration)
    - [GitHub アクション](#running-tests-on-github-actions)

<a name="introduction"></a>
## 導入 (Introduction)

[LaravelPint](https://github.com/laravel/pint) は、ミニマリスト向けの独自の PHP コード スタイル修正ツールです。 Pint は PHP-CS-Fixer の上に構築されており、コード スタイルをクリーンで一貫性のある状態に保つことが簡単になります。

Pint はすべての新しい Laravel アプリケーションとともに自動的にインストールされるため、すぐに使用を開始できます。デフォルトでは、Pint は設定を必要とせず、Laravel の独自のコーディング スタイルに従ってコード内のコード スタイルの問題を修正します。

<a name="installation"></a>
## インストール (Installation)

Pint は Laravel フレームワークの最近のリリースに含まれているため、通常はインストールは必要ありません。ただし、古いアプリケーションの場合は、Composer 経由で Laravel Pint をインストールできます。

```shell
composer require laravel/pint --dev
```

<a name="running-pint"></a>
## ランニングPint (Running Pint)

プロジェクトの `vendor/bin` ディレクトリにある `pint` バイナリを呼び出すことで、コード スタイルの問題を修正するように Pint に指示できます。

```shell
./vendor/bin/pint
```

特定のファイルまたはディレクトリに対して Pint を実行することもできます。

```shell
./vendor/bin/pint app/Models

./vendor/bin/pint app/Models/User.php
```

Pint は、更新するすべてのファイルの完全なリストを表示します。 Pint を呼び出すときに `-v` オプションを指定すると、Pint の変更についてさらに詳細を表示できます。

```shell
./vendor/bin/pint -v
```

実際にファイルを変更せずに、Pint に単にコードのスタイル エラーを検査させたい場合は、`--test` オプションを使用できます。コード スタイル エラーが見つかった場合、Pint はゼロ以外の終了コードを返します。

```shell
./vendor/bin/pint --test
```

Git に従って提供されたブランチと異なるファイルのみを Pint に変更させたい場合は、`--diff=[branch]` オプションを使用できます。これを CI 環境 (GitHub アクションなど) で効果的に使用すると、新しいファイルまたは変更されたファイルのみを検査することで時間を節約できます。

```shell
./vendor/bin/pint --diff=main
```

Git に従ってコミットされていない変更があるファイルのみを Pint に変更させたい場合は、`--dirty` オプションを使用できます。

```shell
./vendor/bin/pint --dirty
```

コード スタイル エラーのあるファイルを Pint に修正させたいが、エラーが修正された場合にはゼロ以外の終了コードで終了するようにしたい場合は、`--repair` オプションを使用できます。

```shell
./vendor/bin/pint --repair
```

<a name="configuring-pint"></a>
## Pint の構成 (Configuring Pint)

前述したように、Pint には構成は必要ありません。ただし、プリセット、ルール、または検査されたフォルダーをカスタマイズしたい場合は、プロジェクトのルート ディレクトリに `pint.json` ファイルを作成することで実行できます。

```json
{
    "preset": "laravel"
}
```

さらに、特定のディレクトリの `pint.json` を使用したい場合は、Pint を呼び出すときに `--config` オプションを指定できます。

```shell
./vendor/bin/pint --config vendor/my-company/coding-style/pint.json
```

<a name="presets"></a>
### プリセット

プリセットは、コード内のコード スタイルの問題を修正するために使用できる一連のルールを定義します。デフォルトでは、Pint は `laravel` プリセットを使用します。これは、Laravel の独自のコーディング スタイルに従うことで問題を修正します。ただし、Pint に `--preset` オプションを指定することで、別のプリセットを指定できます。

```shell
./vendor/bin/pint --preset psr12
```

必要に応じて、プロジェクトの `pint.json` ファイルにプリセットを設定することもできます。

```json
{
    "preset": "psr12"
}
```

Pint で現在サポートされているプリセットは、`laravel`、`per`、`psr12`、`symfony`、および `empty` です。

<a name="rules"></a>
### ルール

ルールは、コード内のコード スタイルの問題を修正するために Pint が使用するスタイル ガイドラインです。上で述べたように、プリセットは、ほとんどの PHP プロジェクトに最適な事前定義されたルールのグループであるため、通常、プリセットに含まれる個々のルールについて心配する必要はありません。

ただし、必要に応じて、`pint.json` ファイルで特定のルールを有効または無効にしたり、`empty` プリセットを使用してルールを最初から定義したりできます。

```json
{
    "preset": "laravel",
    "rules": {
        "simplified_null_return": true,
        "array_indentation": false,
        "new_with_parentheses": {
            "anonymous_class": true,
            "named_class": true
        }
    }
}
```

Pint は [PHP-CS-Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer) の上に構築されています。したがって、そのルールのいずれかを使用して、プロジェクトのコード スタイルの問題を修正できます: [PHP-CS-Fixer コンフィギュレーター](https://mlocati.github.io/php-cs-fixer-configurator)。

<a name="excluding-files-or-folders"></a>
### ファイル/フォルダーの除外

デフォルトでは、Pint は、`vendor` ディレクトリ内のファイルを除く、プロジェクト内のすべての `.php` ファイルを検査します。さらに多くのフォルダーを除外したい場合は、`exclude` 構成オプションを使用して除外できます。

```json
{
    "exclude": [
        "my-specific/folder"
    ]
}
```

特定の名前パターンを含むすべてのファイルを除外したい場合は、`notName` 構成オプションを使用して除外できます。

```json
{
    "notName": [
        "*-my-file.php"
    ]
}
```

ファイルへの正確なパスを指定してファイルを除外したい場合は、`notPath` 構成オプションを使用して実行できます。

```json
{
    "notPath": [
        "path/to/excluded-file.php"
    ]
}
```

<a name="continuous-integration"></a>
## 継続的インテグレーション (Continuous Integration)

<a name="running-tests-on-github-actions"></a>
### GitHub アクション

Laravel Pint を使用してプロジェクトの lint を自動化するには、新しいコードが GitHub にプッシュされるたびに Pint を実行するように [GitHub アクション](https://github.com/features/actions) を構成できます。まず、**[設定] > [アクション] > [一般] > [ワークフロー権限]** で、GitHub 内のワークフローに「読み取りおよび書き込み権限」を付与してください。次に、次の内容の `.github/workflows/lint.yml` ファイルを作成します。

```yaml
name: Fix Code Style

on: [push]

jobs:
  lint:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: true
      matrix:
        php: [8.4]

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: ${{ matrix.php }}
          extensions: json, dom, curl, libxml, mbstring
          coverage: none

      - name: Install Pint
        run: composer global require laravel/pint

      - name: Run Pint
        run: pint

      - name: Commit linted files
        uses: stefanzweifel/git-auto-commit-action@v5
```

