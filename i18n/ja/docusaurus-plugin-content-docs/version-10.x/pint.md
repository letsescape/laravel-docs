# LaravelPint (Laravel Pint)

- [Introduction](#introduction)
- [Installation](#installation)
- [ランニングPint](#running-pint)
- [Pint の構成](#configuring-pint)
    - [Presets](#presets)
    - [Rules](#rules)
    - [ファイル/フォルダーの除外](#excluding-files-or-folders)

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

実際にファイルを変更せずに、Pint に単にコードのスタイル エラーを検査させたい場合は、`--test` オプションを使用できます。

```shell
./vendor/bin/pint --test
```

Git に従ってコミットされていない変更があるファイルのみを Pint に変更させたい場合は、`--dirty` オプションを使用できます。

```shell
./vendor/bin/pint --dirty
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
pint --config vendor/my-company/coding-style/pint.json
```

<a name="presets"></a>
### プリセット

プリセットは、コード内のコード スタイルの問題を修正するために使用できる一連のルールを定義します。デフォルトでは、Pint は `laravel` プリセットを使用します。これは、Laravel の独自のコーディング スタイルに従うことで問題を修正します。ただし、Pint に `--preset` オプションを指定することで、別のプリセットを指定できます。

```shell
pint --preset psr12
```

必要に応じて、プロジェクトの `pint.json` ファイルにプリセットを設定することもできます。

```json
{
    "preset": "psr12"
}
```

Pint で現在サポートされているプリセットは、`laravel`、`per`、`psr12`、および `symfony` です。

<a name="rules"></a>
### ルール

ルールは、コード内のコード スタイルの問題を修正するために Pint が使用するスタイル ガイドラインです。上で述べたように、プリセットは、ほとんどの PHP プロジェクトに最適な事前定義されたルールのグループであるため、通常、プリセットに含まれる個々のルールについて心配する必要はありません。

ただし、必要に応じて、`pint.json` ファイル内の特定のルールを有効または無効にすることができます。

```json
{
    "preset": "laravel",
    "rules": {
        "simplified_null_return": true,
        "braces": false,
        "new_with_braces": {
            "anonymous_class": false,
            "named_class": false
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

