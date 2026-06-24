<!-- # Localization -->
# Localization

- [Introduction](#introduction)
    - [Publishing the Language Files](#publishing-the-language-files)
    - [Configuring the Locale](#configuring-the-locale)
    - [Pluralization Language](#pluralization-language)
- [Defining Translation Strings](#defining-translation-strings)
    - [Using Short Keys](#using-short-keys)
    - [Using Translation Strings as Keys](#using-translation-strings-as-keys)
- [Retrieving Translation Strings](#retrieving-translation-strings)
    - [Replacing Parameters in Translation Strings](#replacing-parameters-in-translation-strings)
    - [Pluralization](#pluralization)
- [Overriding Package Language Files](#overriding-package-language-files)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

> [!NOTE]
> デフォルトでは、Laravel アプリケーションのスケルトンには `lang` ディレクトリが含まれません。 Laravel の言語ファイルをカスタマイズしたい場合は、`lang:publish` Artisan コマンドを使用して言語ファイルを公開できます。

<!-- Laravel's localization features provide a convenient way to retrieve strings in various languages, allowing you to easily support multiple languages within your application. -->
Laravel のローカリゼーション機能は、さまざまな言語で文字列を取得する便利な方法を提供し、アプリケーション内で複数の言語を簡単にサポートできるようにします。

<!-- Laravel provides two ways to manage translation strings. First, language strings may be stored in files within the application's `lang` directory. Within this directory, there may be subdirectories for each language supported by the application. This is the approach Laravel uses to manage translation strings for built-in Laravel features such as validation error messages: -->
Laravel では、翻訳文字列を管理する 2 つの方法が提供されています。まず、言語文字列はアプリケーションの `lang` ディレクトリ内のファイルに保存されます。このディレクトリ内には、アプリケーションでサポートされている言語ごとにサブディレクトリが存在する場合があります。これは、検証エラーメッセージなどの組み込みの Laravel 機能の翻訳文字列を管理するために Laravel が使用するアプローチです。

```text
/lang
    /en
        messages.php
    /es
        messages.php
```

<!-- Or, translation strings may be defined within JSON files that are placed within the `lang` directory. When taking this approach, each language supported by your application would have a corresponding JSON file within this directory. This approach is recommended for applications that have a large number of translatable strings: -->
または、変換文字列は、`lang` ディレクトリ内に配置された JSON ファイル内で定義できます。このアプローチを採用する場合、アプリケーションでサポートされる各言語には、このディレクトリ内に対応する JSON ファイルが存在します。このアプローチは、翻訳可能な文字列が多数あるアプリケーションに推奨されます。

```text
/lang
    en.json
    es.json
```

<!-- We'll discuss each approach to managing translation strings within this documentation. -->
このドキュメントでは、翻訳文字列を管理するためのそれぞれのアプローチについて説明します。

<a name="publishing-the-language-files"></a>
<!-- ### Publishing the Language Files -->
### Publishing the Language Files

<!-- By default, the Laravel application skeleton does not include the `lang` directory. If you would like to customize Laravel's language files or create your own, you should scaffold the `lang` directory via the `lang:publish` Artisan command. The `lang:publish` command will create the `lang` directory in your application and publish the default set of language files used by Laravel: -->
デフォルトでは、Laravel アプリケーションのスケルトンには `lang` ディレクトリが含まれません。 Laravel の言語ファイルをカスタマイズするか、独自の言語ファイルを作成したい場合は、`lang:publish` Artisan コマンドを使用して `lang` ディレクトリをスキャフォールディングする必要があります。 `lang:publish` コマンドは、アプリケーション内に `lang` ディレクトリを作成し、Laravel で使用される言語ファイルのデフォルトのセットを公開します。

```shell
php artisan lang:publish
```

<a name="configuring-the-locale"></a>
<!-- ### Configuring the Locale -->
### Configuring the Locale

<!-- The default language for your application is stored in the `config/app.php` configuration file's `locale` configuration option, which is typically set using the `APP_LOCALE` environment variable. You are free to modify this value to suit the needs of your application. -->
アプリケーションのデフォルト言語は、`config/app.php` 構成ファイルの `locale` 構成オプションに保存されます。これは通常、`APP_LOCALE` 環境変数を使用して設定されます。アプリケーションのニーズに合わせてこの値を自由に変更できます。

<!-- You may also configure a "fallback language", which will be used when the default language does not contain a given translation string. Like the default language, the fallback language is also configured in the `config/app.php` configuration file, and its value is typically set using the `APP_FALLBACK_LOCALE` environment variable. -->
また、デフォルト言語に特定の翻訳文字列が含まれていない場合に使用される「フォールバック言語」を構成することもできます。デフォルト言語と同様に、フォールバック言語も `config/app.php` 構成ファイルで構成され、その値は通常、`APP_FALLBACK_LOCALE` 環境変数を使用して設定されます。

<!-- You may modify the default language for a single HTTP request at runtime using the `setLocale` method provided by the `App` facade: -->
`App` ファサードによって提供される `setLocale` メソッドを使用して、実行時に単一の HTTP リクエストのデフォルト言語を変更できます。

```php
use Illuminate\Support\Facades\App;

Route::get('/greeting/{locale}', function (string $locale) {
    if (! in_array($locale, ['en', 'es', 'fr'])) {
        abort(400);
    }

    App::setLocale($locale);

    // ...
});
```

<a name="determining-the-current-locale"></a>
<!-- #### Determining the Current Locale -->
#### Determining the Current Locale

<!-- You may use the `currentLocale` and `isLocale` methods on the `App` facade to determine the current locale or check if the locale is a given value: -->
`App` ファサードで `currentLocale` メソッドと `isLocale` メソッドを使用して、現在のロケールを確認したり、ロケールが指定された値であるかどうかを確認したりできます。

```php
use Illuminate\Support\Facades\App;

$locale = App::currentLocale();

if (App::isLocale('en')) {
    // ...
}
```

<a name="pluralization-language"></a>
<!-- ### Pluralization Language -->
### Pluralization Language

<!-- <div class="code-list-no-flex-break"> -->
<div class="code-list-no-flex-break">

<!-- You may instruct Laravel's "pluralizer", which is used by Eloquent and other portions of the framework to convert singular strings to plural strings, to use a language other than English. This may be accomplished by invoking the `useLanguage` method within the `boot` method of one of your application's service providers. The pluralizer's currently supported languages are: `french`, `norwegian-bokmal`, `portuguese`, `spanish`, and `turkish`: -->
Eloquent やフレームワークの他の部分で単数文字列を複数文字列に変換するために使用される Laravel の「pluralizer」に、英語以外の言語を使用するように指示できます。これは、アプリケーションのサービスプロバイダの 1 つの `boot` メソッド内で `useLanguage` メソッドを呼び出すことで実現できます。 pluralizer で現在サポートされている言語は、`french`、`norwegian-bokmal`、`portuguese`、`spanish`、および `turkish` です。

<!-- </div> -->
</div>

```php
use Illuminate\Support\Pluralizer;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Pluralizer::useLanguage('spanish');

    // ...
}
```

> [!WARNING]
> pluralizer の言語をカスタマイズする場合は、Eloquent モデルの [table names](/docs/13.x/eloquent#table-names) を明示的に定義する必要があります。

<a name="defining-translation-strings"></a>
<!-- ## Defining Translation Strings -->
## Defining Translation Strings

<a name="using-short-keys"></a>
<!-- ### Using Short Keys -->
### Using Short Keys

<!-- Typically, translation strings are stored in files within the `lang` directory. Within this directory, there should be a subdirectory for each language supported by your application. This is the approach Laravel uses to manage translation strings for built-in Laravel features such as validation error messages: -->
通常、翻訳文字列は、`lang` ディレクトリ内のファイルに保存されます。このディレクトリ内には、アプリケーションでサポートされている言語ごとにサブディレクトリが存在する必要があります。これは、検証エラーメッセージなどの組み込みの Laravel 機能の翻訳文字列を管理するために Laravel が使用するアプローチです。

```text
/lang
    /en
        messages.php
    /es
        messages.php
```

<!-- All language files return an array of keyed strings. For example: -->
すべての言語ファイルは、キー付き文字列の配列を返します。例えば：

```php
<?php

// lang/en/messages.php

return [
    'welcome' => 'Welcome to our application!',
];
```

> [!WARNING]
> 地域によって異なる言語の場合は、ISO 15897 に従って言語ディレクトリに名前を付ける必要があります。たとえば、イギリス英語には「en-gb」ではなく「en_GB」を使用する必要があります。

<a name="using-translation-strings-as-keys"></a>
<!-- ### Using Translation Strings as Keys -->
### Using Translation Strings as Keys

<!-- For applications with a large number of translatable strings, defining every string with a "short key" can become confusing when referencing the keys in your views and it is cumbersome to continually invent keys for every translation string supported by your application. -->
翻訳可能な文字列が多数あるアプリケーションの場合、すべての文字列を「短いキー」で定義すると、ビューでキーを参照するときに混乱が生じる可能性があり、アプリケーションでサポートされているすべての翻訳文字列に対してキーを継続的に作成するのは面倒です。

<!-- For this reason, Laravel also provides support for defining translation strings using the "default" translation of the string as the key. Language files that use translation strings as keys are stored as JSON files in the `lang` directory. For example, if your application has a Spanish translation, you should create a `lang/es.json` file: -->
このため、Laravel は、文字列の「デフォルト」翻訳をキーとして使用して翻訳文字列を定義するためのサポートも提供します。翻訳文字列をキーとして使用する言語ファイルは、`lang` ディレクトリに JSON ファイルとして保存されます。たとえば、アプリケーションにスペイン語への翻訳がある場合は、`lang/es.json` ファイルを作成する必要があります。

```json
{
    "I love programming.": "Me encanta programar."
}
```

<!-- #### Key / File Conflicts -->
#### Key / File Conflicts

<!-- You should not define translation string keys that conflict with other translation filenames. For example, translating `__('Action')` for the "NL" locale while a `nl/action.php` file exists but a `nl.json` file does not exist will result in the translator returning the entire contents of `nl/action.php`. -->
他の翻訳ファイル名と競合する翻訳文字列キーを定義しないでください。たとえば、`nl/action.php` ファイルは存在するが、`nl.json` ファイルが存在しないときに、「NL」ロケールの `__('Action')` を翻訳すると、トランスレータは `nl/action.php` の内容全体を返すことになります。

<a name="retrieving-translation-strings"></a>
<!-- ## Retrieving Translation Strings -->
## Retrieving Translation Strings

<!-- You may retrieve translation strings from your language files using the `__` helper function. If you are using "short keys" to define your translation strings, you should pass the file that contains the key and the key itself to the `__` function using "dot" syntax. For example, let's retrieve the `welcome` translation string from the `lang/en/messages.php` language file: -->
`__` ヘルパ関数を使用して、言語ファイルから翻訳文字列を取得できます。 「短いキー」を使用して翻訳文字列を定義している場合は、「ドット」構文を使用して、キーを含むファイルとキー自体を `__` 関数に渡す必要があります。たとえば、`lang/en/messages.php` 言語ファイルから `welcome` 翻訳文字列を取得してみましょう。

```php
echo __('messages.welcome');
```

<!-- If the specified translation string does not exist, the `__` function will return the translation string key. So, using the example above, the `__` function would return `messages.welcome` if the translation string does not exist. -->
指定された翻訳文字列が存在しない場合、`__` 関数は翻訳文字列キーを返します。したがって、上記の例を使用すると、変換文字列が存在しない場合、`__` 関数は `messages.welcome` を返します。

<!-- If you are using your [default translation strings as your translation keys](#using-translation-strings-as-keys), you should pass the default translation of your string to the `__` function; -->
[default translation strings as your translation keys](#using-translation-strings-as-keys) を使用している場合は、文字列のデフォルトの翻訳を `__` 関数に渡す必要があります。

```php
echo __('I love programming.');
```

<!-- Again, if the translation string does not exist, the `__` function will return the translation string key that it was given. -->
繰り返しますが、翻訳文字列が存在しない場合、`__` 関数は、指定された翻訳文字列キーを返します。

<!-- If you are using the [Blade templating engine](/docs/13.x/blade), you may use the `{{ }}` echo syntax to display the translation string: -->
[Blade templating engine](/docs/13.x/blade) を使用している場合は、`{{ }}` エコー構文を使用して翻訳文字列を表示できます。

```blade
{{ __('messages.welcome') }}
```

<a name="replacing-parameters-in-translation-strings"></a>
<!-- ### Replacing Parameters in Translation Strings -->
### Replacing Parameters in Translation Strings

<!-- If you wish, you may define placeholders in your translation strings. All placeholders are prefixed with a `:`. For example, you may define a welcome message with a placeholder name: -->
必要に応じて、翻訳文字列にプレースホルダーを定義できます。すべてのプレースホルダーには `:` という接頭辞が付けられます。たとえば、プレースホルダー名を使用してウェルカム メッセージを定義できます。

```php
'welcome' => 'Welcome, :name',
```

<!-- To replace the placeholders when retrieving a translation string, you may pass an array of replacements as the second argument to the `__` function: -->
翻訳文字列を取得するときにプレースホルダーを置換するには、置換文字列の配列を 2 番目の引数として `__` 関数に渡します。

```php
echo __('messages.welcome', ['name' => 'dayle']);
```

<!-- If your placeholder contains all capital letters, or only has its first letter capitalized, the translated value will be capitalized accordingly: -->
プレースホルダーにすべて大文字が含まれている場合、または最初の文字のみが大文字である場合、翻訳された値はそれに応じて大文字になります。

```php
'welcome' => 'Welcome, :NAME', // Welcome, DAYLE
'goodbye' => 'Goodbye, :Name', // Goodbye, Dayle
```

<a name="object-replacement-formatting"></a>
<!-- #### Object Replacement Formatting -->
#### Object Replacement Formatting

<!-- If you attempt to provide an object as a translation placeholder, the object's `__toString` method will be invoked. The [__toString](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) method is one of PHP's built-in "magic methods". However, sometimes you may not have control over the `__toString` method of a given class, such as when the class that you are interacting with belongs to a third-party library. -->
オブジェクトを翻訳プレースホルダーとして提供しようとすると、オブジェクトの `__toString` メソッドが呼び出されます。 [__toString](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) メソッドは、PHP の組み込み「マジック メソッド」の 1 つです。ただし、対話しているクラスがサードパーティのライブラリに属している場合など、特定のクラスの `__toString` メソッドを制御できない場合があります。

<!-- In these cases, Laravel allows you to register a custom formatting handler for that particular type of object. To accomplish this, you should invoke the translator's `stringable` method. The `stringable` method accepts a closure, which should type-hint the type of object that it is responsible for formatting. Typically, the `stringable` method should be invoked within the `boot` method of your application's `AppServiceProvider` class: -->
このような場合、Laravel では、その特定の種類のオブジェクトにカスタム書式設定ハンドラーを登録できます。これを実現するには、トランスレーターの `stringable` メソッドを呼び出す必要があります。 `stringable` メソッドはクロージャを受け入れます。クロージャは、書式設定を担当するオブジェクトのタイプをタイプヒントする必要があります。通常、`stringable` メソッドは、アプリケーションの `AppServiceProvider` クラスの `boot` メソッド内で呼び出す必要があります。

```php
use Illuminate\Support\Facades\Lang;
use Money\Money;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Lang::stringable(function (Money $money) {
        return $money->formatTo('en_GB');
    });
}
```

<a name="pluralization"></a>
<!-- ### Pluralization -->
### Pluralization

<!-- Pluralization is a complex problem, as different languages have a variety of complex rules for pluralization; however, Laravel can help you translate strings differently based on pluralization rules that you define. Using a `|` character, you may distinguish singular and plural forms of a string: -->
言語ごとに複数化に関するさまざまな複雑なルールがあるため、複数化は複雑な問題です。ただし、Laravel は、定義した複数形ルールに基づいて文字列を異なる方法で変換するのに役立ちます。 `|` 文字を使用すると、文字列の単数形と複数形を区別できます。

```php
'apples' => 'There is one apple|There are many apples',
```

<!-- Of course, pluralization is also supported when using [translation strings as keys](#using-translation-strings-as-keys): -->
もちろん、[translation strings as keys](#using-translation-strings-as-keys) を使用する場合は複数形もサポートされます。

```json
{
    "There is one apple|There are many apples": "Hay una manzana|Hay muchas manzanas"
}
```

<!-- You may even create more complex pluralization rules which specify translation strings for multiple ranges of values: -->
複数の値範囲の翻訳文字列を指定する、より複雑な複数形化ルールを作成することもできます。

```php
'apples' => '{0} There are none|[1,19] There are some|[20,*] There are many',
```

<!-- After defining a translation string that has pluralization options, you may use the `trans_choice` function to retrieve the line for a given "count". In this example, since the count is greater than one, the plural form of the translation string is returned: -->
複数形化オプションを持つ翻訳文字列を定義した後、`trans_choice` 関数を使用して、指定された「カウント」の行を取得できます。この例では、カウントが 1 より大きいため、翻訳文字列の複数形が返されます。

```php
echo trans_choice('messages.apples', 10);
```

<!-- You may also define placeholder attributes in pluralization strings. These placeholders may be replaced by passing an array as the third argument to the `trans_choice` function: -->
複数形文字列でプレースホルダー属性を定義することもできます。これらのプレースホルダーは、配列を `trans_choice` 関数の 3 番目の引数として渡すことで置き換えることができます。

```php
'minutes_ago' => '{1} :value minute ago|[2,*] :value minutes ago',

echo trans_choice('time.minutes_ago', 5, ['value' => 5]);
```

<!-- If you would like to display the integer value that was passed to the `trans_choice` function, you may use the built-in `:count` placeholder: -->
`trans_choice` 関数に渡された整数値を表示したい場合は、組み込みの `:count` プレースホルダーを使用できます。

```php
'apples' => '{0} There are none|{1} There is one|[2,*] There are :count',
```

<a name="overriding-package-language-files"></a>
<!-- ## Overriding Package Language Files -->
## Overriding Package Language Files

<!-- Some packages may ship with their own language files. Instead of changing the package's core files to tweak these lines, you may override them by placing files in the `lang/vendor/{package}/{locale}` directory. -->
一部のパッケージには独自の言語ファイルが同梱されている場合があります。パッケージのコア ファイルを変更してこれらの行を調整する代わりに、`lang/vendor/{package}/{locale}` ディレクトリにファイルを配置することでそれらをオーバーライドできます。

<!-- So, for example, if you need to override the English translation strings in `messages.php` for a package named `skyrim/hearthfire`, you should place a language file at: `lang/vendor/hearthfire/en/messages.php`. Within this file, you should only define the translation strings you wish to override. Any translation strings you don't override will still be loaded from the package's original language files. -->
したがって、たとえば、`skyrim/hearthfire` という名前のパッケージの `messages.php` 内の英語翻訳文字列をオーバーライドする必要がある場合は、言語ファイルを `lang/vendor/hearthfire/en/messages.php` に配置する必要があります。このファイル内では、オーバーライドする翻訳文字列のみを定義する必要があります。オーバーライドしない翻訳文字列は、パッケージの元の言語ファイルから読み込まれます。

