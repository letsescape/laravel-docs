<!-- # Laravel Pint -->
# Laravel Pint

- [Introduction](#introduction)
- [Installation](#installation)
- [Running Pint](#running-pint)
- [Configuring Pint](#configuring-pint)
    - [Presets](#presets)
    - [Rules](#rules)
    - [Excluding Files / Folders](#excluding-files-or-folders)
- [Continuous Integration](#continuous-integration)
    - [GitHub Actions](#running-tests-on-github-actions)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Pint](https://github.com/laravel/pint) is an opinionated PHP code style fixer for minimalists. Pint is built on top of PHP-CS-Fixer and makes it simple to ensure that your code style stays clean and consistent. -->
[Laravel Pint](https://github.com/laravel/pint) は、ミニマリスト向けの独自の PHP コード スタイル修正ツールです。 Pint は PHP-CS-Fixer の上に構築されており、コード スタイルをクリーンで一貫性のある状態に保つことが簡単になります。

<!-- Pint is automatically installed with all new Laravel applications so you may start using it immediately. By default, Pint does not require any configuration and will fix code style issues in your code by following the opinionated coding style of Laravel. -->
Pint はすべての新しい Laravel アプリケーションとともに自動的にインストールされるため、すぐに使用を開始できます。デフォルトでは、Pint は設定を必要とせず、Laravel の独自のコーディング スタイルに従ってコード内のコード スタイルの問題を修正します。

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- Pint is included in recent releases of the Laravel framework, so installation is typically unnecessary. However, for older applications, you may install Laravel Pint via Composer: -->
Pint は Laravel フレームワークの最近のリリースに含まれているため、通常はインストールは必要ありません。ただし、古いアプリケーションの場合は、Composer 経由で Laravel Pint をインストールできます。

```shell
composer require laravel/pint --dev
```

<a name="running-pint"></a>
<!-- ## Running Pint -->
## Running Pint

<!-- You can instruct Pint to fix code style issues by invoking the `pint` binary that is available in your project's `vendor/bin` directory: -->
プロジェクトの `vendor/bin` ディレクトリにある `pint` バイナリを呼び出すことで、コード スタイルの問題を修正するように Pint に指示できます。

```shell
./vendor/bin/pint
```

<!-- You may also run Pint on specific files or directories: -->
特定のファイルまたはディレクトリに対して Pint を実行することもできます。

```shell
./vendor/bin/pint app/Models

./vendor/bin/pint app/Models/User.php
```

<!-- Pint will display a thorough list of all of the files that it updates. You can view even more detail about Pint's changes by providing the `-v` option when invoking Pint: -->
Pint は、更新するすべてのファイルの完全なリストを表示します。 Pint を呼び出すときに `-v` オプションを指定すると、Pint の変更についてさらに詳細を表示できます。

```shell
./vendor/bin/pint -v
```

<!-- If you would like Pint to simply inspect your code for style errors without actually changing the files, you may use the `--test` option. Pint will return a non-zero exit code if any code style errors are found: -->
実際にファイルを変更せずに、Pint に単にコードのスタイル エラーを検査させたい場合は、`--test` オプションを使用できます。コード スタイル エラーが見つかった場合、Pint はゼロ以外の終了コードを返します。

```shell
./vendor/bin/pint --test
```

<!-- If you would like Pint to only modify the files that differ from the provided branch according to Git, you may use the `--diff=[branch]` option. This can be effectively used in your CI environment (like GitHub actions) to save time by only inspecting new or modified files: -->
Git に従って提供されたブランチと異なるファイルのみを Pint に変更させたい場合は、`--diff=[branch]` オプションを使用できます。これを CI 環境 (GitHub アクションなど) で効果的に使用すると、新しいファイルまたは変更されたファイルのみを検査することで時間を節約できます。

```shell
./vendor/bin/pint --diff=main
```

<!-- If you would like Pint to only modify the files that have uncommitted changes according to Git, you may use the `--dirty` option: -->
Git に従ってコミットされていない変更があるファイルのみを Pint に変更させたい場合は、`--dirty` オプションを使用できます。

```shell
./vendor/bin/pint --dirty
```

<!-- If you would like Pint to fix any files with code style errors but also exit with a non-zero exit code if any errors were fixed, you may use the `--repair` option: -->
コード スタイル エラーのあるファイルを Pint に修正させたいが、エラーが修正された場合にはゼロ以外の終了コードで終了するようにしたい場合は、`--repair` オプションを使用できます。

```shell
./vendor/bin/pint --repair
```

<a name="configuring-pint"></a>
<!-- ## Configuring Pint -->
## Configuring Pint

<!-- As previously mentioned, Pint does not require any configuration. However, if you wish to customize the presets, rules, or inspected folders, you may do so by creating a `pint.json` file in your project's root directory: -->
前述したように、Pint には構成は必要ありません。ただし、プリセット、ルール、または検査されたフォルダーをカスタマイズしたい場合は、プロジェクトのルート ディレクトリに `pint.json` ファイルを作成することで実行できます。

```json
{
    "preset": "laravel"
}
```

<!-- In addition, if you wish to use a `pint.json` from a specific directory, you may provide the `--config` option when invoking Pint: -->
さらに、特定のディレクトリの `pint.json` を使用したい場合は、Pint を呼び出すときに `--config` オプションを指定できます。

```shell
./vendor/bin/pint --config vendor/my-company/coding-style/pint.json
```

<a name="presets"></a>
<!-- ### Presets -->
### Presets

<!-- Presets define a set of rules that can be used to fix code style issues in your code. By default, Pint uses the `laravel` preset, which fixes issues by following the opinionated coding style of Laravel. However, you may specify a different preset by providing the `--preset` option to Pint: -->
プリセットは、コード内のコード スタイルの問題を修正するために使用できる一連のルールを定義します。デフォルトでは、Pint は `laravel` プリセットを使用します。これは、Laravel の独自のコーディング スタイルに従うことで問題を修正します。ただし、Pint に `--preset` オプションを指定することで、別のプリセットを指定できます。

```shell
./vendor/bin/pint --preset psr12
```

<!-- If you wish, you may also set the preset in your project's `pint.json` file: -->
必要に応じて、プロジェクトの `pint.json` ファイルにプリセットを設定することもできます。

```json
{
    "preset": "psr12"
}
```

<!-- Pint's currently supported presets are: `laravel`, `per`, `psr12`, `symfony`, and `empty`. -->
Pint で現在サポートされているプリセットは、`laravel`、`per`、`psr12`、`symfony`、および `empty` です。

<a name="rules"></a>
<!-- ### Rules -->
### Rules

<!-- Rules are style guidelines that Pint will use to fix code style issues in your code. As mentioned above, presets are predefined groups of rules that should be perfect for most PHP projects, so you typically will not need to worry about the individual rules they contain. -->
ルールは、コード内のコード スタイルの問題を修正するために Pint が使用するスタイル ガイドラインです。上で述べたように、プリセットは、ほとんどの PHP プロジェクトに最適な事前定義されたルールのグループであるため、通常、プリセットに含まれる個々のルールについて心配する必要はありません。

<!-- However, if you wish, you may enable or disable specific rules in your `pint.json` file or use the `empty` preset and define the rules from scratch: -->
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

<!-- Pint is built on top of [PHP-CS-Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer). Therefore, you may use any of its rules to fix code style issues in your project: [PHP-CS-Fixer Configurator](https://mlocati.github.io/php-cs-fixer-configurator). -->
Pint は [PHP-CS-Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer) の上に構築されています。したがって、そのルールのいずれかを使用して、プロジェクトのコード スタイルの問題を修正できます: [PHP-CS-Fixer Configurator](https://mlocati.github.io/php-cs-fixer-configurator)。

<a name="excluding-files-or-folders"></a>
<!-- ### Excluding Files / Folders -->
### Excluding Files / Folders

<!-- By default, Pint will inspect all `.php` files in your project except those in the `vendor` directory. If you wish to exclude more folders, you may do so using the `exclude` configuration option: -->
デフォルトでは、Pint は、`vendor` ディレクトリ内のファイルを除く、プロジェクト内のすべての `.php` ファイルを検査します。さらに多くのフォルダーを除外したい場合は、`exclude` 構成オプションを使用して除外できます。

```json
{
    "exclude": [
        "my-specific/folder"
    ]
}
```

<!-- If you wish to exclude all files that contain a given name pattern, you may do so using the `notName` configuration option: -->
特定の名前パターンを含むすべてのファイルを除外したい場合は、`notName` 構成オプションを使用して除外できます。

```json
{
    "notName": [
        "*-my-file.php"
    ]
}
```

<!-- If you would like to exclude a file by providing an exact path to the file, you may do so using the `notPath` configuration option: -->
ファイルへの正確なパスを指定してファイルを除外したい場合は、`notPath` 構成オプションを使用して実行できます。

```json
{
    "notPath": [
        "path/to/excluded-file.php"
    ]
}
```

<a name="continuous-integration"></a>
<!-- ## Continuous Integration -->
## Continuous Integration

<a name="running-tests-on-github-actions"></a>
<!-- ### GitHub Actions -->
### GitHub Actions

<!-- To automate linting your project with Laravel Pint, you can configure [GitHub Actions](https://github.com/features/actions) to run Pint whenever new code is pushed to GitHub. First, be sure to grant "Read and write permissions" to workflows within GitHub at **Settings > Actions > General > Workflow permissions**. Then, create a `.github/workflows/lint.yml` file with the following content: -->
Laravel Pint を使用してプロジェクトの lint を自動化するには、新しいコードが GitHub にプッシュされるたびに Pint を実行するように [GitHub Actions](https://github.com/features/actions) を構成できます。まず、**[設定] > [アクション] > [一般] > [ワークフロー権限]** で、GitHub 内のワークフローに「読み取りおよび書き込み権限」を付与してください。次に、次の内容の `.github/workflows/lint.yml` ファイルを作成します。

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

