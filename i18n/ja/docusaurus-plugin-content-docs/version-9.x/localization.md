# ローカリゼーション (Localization)

- [Introduction](#introduction)
    - [ロケールの構成](#configuring-the-locale)
    - [複数化言語](#pluralization-language)
- [翻訳文字列の定義](#defining-translation-strings)
    - [ショートキーの使用](#using-short-keys)
    - [翻訳文字列をキーとして使用する](#using-translation-strings-as-keys)
- [翻訳文字列の取得](#retrieving-translation-strings)
    - [翻訳文字列内のパラメータの置換](#replacing-parameters-in-translation-strings)
    - [Pluralization](#pluralization)
- [パッケージ言語ファイルの上書き](#overriding-package-language-files)

<a name="introduction"></a>
## 導入 (Introduction)

Laravel のローカリゼーション機能は、さまざまな言語で文字列を取得する便利な方法を提供し、アプリケーション内で複数の言語を簡単にサポートできるようにします。

Laravel では、翻訳文字列を管理する 2 つの方法が提供されています。まず、言語文字列は `lang` ディレクトリ内のファイルに保存されます。このディレクトリ内には、アプリケーションでサポートされている言語ごとにサブディレクトリが存在する場合があります。これは、検証エラーメッセージなどの組み込みの Laravel 機能の翻訳文字列を管理するために Laravel が使用するアプローチです。

    /lang
        /en
            messages.php
        /es
            messages.php

または、変換文字列は、`lang` ディレクトリ内に配置された JSON ファイル内で定義できます。このアプローチを採用する場合、アプリケーションでサポートされる各言語には、このディレクトリ内に対応する JSON ファイルが存在します。このアプローチは、翻訳可能な文字列が多数あるアプリケーションに推奨されます。

    /lang
        en.json
        es.json

このドキュメントでは、翻訳文字列を管理するためのそれぞれのアプローチについて説明します。

<a name="configuring-the-locale"></a>
### ロケールの構成

アプリケーションのデフォルト言語は、`config/app.php` 構成ファイルの `locale` 構成オプションに保存されます。アプリケーションのニーズに合わせてこの値を自由に変更できます。

`App` ファサードによって提供される `setLocale` メソッドを使用して、実行時に単一の HTTP リクエストのデフォルト言語を変更できます。

    use Illuminate\Support\Facades\App;

    Route::get('/greeting/{locale}', function ($locale) {
        if (! in_array($locale, ['en', 'es', 'fr'])) {
            abort(400);
        }

        App::setLocale($locale);

        //
    });

「フォールバック言語」を設定できます。これは、アクティブな言語に特定の翻訳文字列が含まれていない場合に使用されます。デフォルト言語と同様に、フォールバック言語も `config/app.php` 構成ファイルで構成されます。

    'fallback_locale' => 'en',

<a name="determining-the-current-locale"></a>
#### 現在のロケールの決定

`App` ファサードで `currentLocale` メソッドと `isLocale` メソッドを使用して、現在のロケールを確認したり、ロケールが指定された値であるかどうかを確認したりできます。

    use Illuminate\Support\Facades\App;

    $locale = App::currentLocale();

    if (App::isLocale('en')) {
        //
    }

<a name="pluralization-language"></a>
### 複数化言語

Eloquent やフレームワークの他の部分で単数文字列を複数文字列に変換するために使用される Laravel の「pluralizer」に、英語以外の言語を使用するように指示できます。これは、アプリケーションのサービスプロバイダの 1 つの `boot` メソッド内で `useLanguage` メソッドを呼び出すことで実現できます。 pluralizer で現在サポートされている言語は、`french`、`norwegian-bokmal`、`portuguese`、`spanish`、および `turkish` です。

    use Illuminate\Support\Pluralizer;

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        Pluralizer::useLanguage('spanish');     

        // ...     
    }

> **警告**
> pluralizer の言語をカスタマイズする場合は、Eloquent モデルの [テーブル名](/docs/{{version}}/eloquent#table-names) を明示的に定義する必要があります。

<a name="defining-translation-strings"></a>
## 翻訳文字列の定義 (Defining Translation Strings)

<a name="using-short-keys"></a>
### ショートキーの使用

通常、翻訳文字列は、`lang` ディレクトリ内のファイルに保存されます。このディレクトリ内には、アプリケーションでサポートされている言語ごとにサブディレクトリが存在する必要があります。これは、検証エラーメッセージなどの組み込みの Laravel 機能の翻訳文字列を管理するために Laravel が使用するアプローチです。

    /lang
        /en
            messages.php
        /es
            messages.php

すべての言語ファイルは、キー付き文字列の配列を返します。例えば：

    <?php

    // lang/en/messages.php

    return [
        'welcome' => 'Welcome to our application!',
    ];

> **警告**
> 地域によって異なる言語の場合は、ISO 15897 に従って言語ディレクトリに名前を付ける必要があります。たとえば、イギリス英語には「en-gb」ではなく「en_GB」を使用する必要があります。

<a name="using-translation-strings-as-keys"></a>
### 翻訳文字列をキーとして使用する

翻訳可能な文字列が多数あるアプリケーションの場合、すべての文字列を「短いキー」で定義すると、ビューでキーを参照するときに混乱が生じる可能性があり、アプリケーションでサポートされているすべての翻訳文字列に対してキーを継続的に作成するのは面倒です。

このため、Laravel は、文字列の「デフォルト」翻訳をキーとして使用して翻訳文字列を定義するためのサポートも提供します。翻訳文字列をキーとして使用する翻訳ファイルは、`lang` ディレクトリに JSON ファイルとして保存されます。たとえば、アプリケーションにスペイン語への翻訳がある場合は、`lang/es.json` ファイルを作成する必要があります。

```json
{
    "I love programming.": "Me encanta programar."
}
```

#### キー/ファイルの競合

他の翻訳ファイル名と競合する翻訳文字列キーを定義しないでください。たとえば、`nl/action.php` ファイルは存在するが、`nl.json` ファイルが存在しないときに、「NL」ロケールの `__('Action')` を翻訳すると、トランスレータは `nl/action.php` の内容を返します。

<a name="retrieving-translation-strings"></a>
## 翻訳文字列の取得 (Retrieving Translation Strings)

`__` ヘルパ関数を使用して、言語ファイルから翻訳文字列を取得できます。 「短いキー」を使用して翻訳文字列を定義している場合は、「ドット」構文を使用して、キーを含むファイルとキー自体を `__` 関数に渡す必要があります。たとえば、`lang/en/messages.php` 言語ファイルから `welcome` 翻訳文字列を取得してみましょう。

    echo __('messages.welcome');

指定された翻訳文字列が存在しない場合、`__` 関数は翻訳文字列キーを返します。したがって、上記の例を使用すると、変換文字列が存在しない場合、`__` 関数は `messages.welcome` を返します。

[デフォルトの翻訳文字列を翻訳キーとして使用する](#using-translation-strings-as-keys) を使用している場合は、文字列のデフォルトの翻訳を `__` 関数に渡す必要があります。

    echo __('I love programming.');

繰り返しますが、翻訳文字列が存在しない場合、`__` 関数は、指定された翻訳文字列キーを返します。

[Blade テンプレートエンジン](/docs/{{version}}/blade) を使用している場合は、`{{ }}` エコー構文を使用して翻訳文字列を表示できます。

    {{ __('messages.welcome') }}

<a name="replacing-parameters-in-translation-strings"></a>
### 翻訳文字列内のパラメータの置換

必要に応じて、翻訳文字列にプレースホルダーを定義できます。すべてのプレースホルダーには `:` という接頭辞が付けられます。たとえば、プレースホルダー名を使用してウェルカム メッセージを定義できます。

    'welcome' => 'Welcome, :name',

翻訳文字列を取得するときにプレースホルダーを置換するには、置換文字列の配列を 2 番目の引数として `__` 関数に渡します。

    echo __('messages.welcome', ['name' => 'dayle']);

プレースホルダーにすべて大文字が含まれている場合、または最初の文字のみが大文字である場合、翻訳された値はそれに応じて大文字になります。

    'welcome' => 'Welcome, :NAME', // Welcome, DAYLE
    'goodbye' => 'Goodbye, :Name', // Goodbye, Dayle

<a name="object-replacement-formatting"></a>
#### オブジェクト置換の書式設定

オブジェクトを翻訳プレースホルダーとして提供しようとすると、オブジェクトの `__toString` メソッドが呼び出されます。 [`__toString`](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) メソッドは、PHP の組み込み「マジック メソッド」の 1 つです。ただし、対話しているクラスがサードパーティのライブラリに属している場合など、特定のクラスの `__toString` メソッドを制御できない場合があります。

このような場合、Laravel では、その特定の種類のオブジェクトにカスタム書式設定ハンドラーを登録できます。これを実現するには、トランスレーターの `stringable` メソッドを呼び出す必要があります。 `stringable` メソッドはクロージャを受け入れます。クロージャは、書式設定を担当するオブジェクトのタイプをタイプヒントする必要があります。通常、`stringable` メソッドは、アプリケーションの `AppServiceProvider` クラスの `boot` メソッド内で呼び出す必要があります。

    use Illuminate\Support\Facades\Lang;
    use Money\Money;

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        Lang::stringable(function (Money $money) {
            return $money->formatTo('en_GB');
        });
    }

<a name="pluralization"></a>
### 複数化

言語ごとに複数化に関するさまざまな複雑なルールがあるため、複数化は複雑な問題です。ただし、Laravel は、定義した複数形ルールに基づいて文字列を異なる方法で変換するのに役立ちます。 `|` 文字を使用すると、文字列の単数形と複数形を区別できます。

    'apples' => 'There is one apple|There are many apples',

もちろん、[翻訳文字列をキーとして使用する](#using-translation-strings-as-keys) を使用する場合は複数形もサポートされます。

```json
{
    "There is one apple|There are many apples": "Hay una manzana|Hay muchas manzanas"
}
```

複数の値範囲の翻訳文字列を指定する、より複雑な複数形化ルールを作成することもできます。

    'apples' => '{0} There are none|[1,19] There are some|[20,*] There are many',

複数形化オプションを持つ翻訳文字列を定義した後、`trans_choice` 関数を使用して、指定された「カウント」の行を取得できます。この例では、カウントが 1 より大きいため、翻訳文字列の複数形が返されます。

    echo trans_choice('messages.apples', 10);

複数形文字列でプレースホルダー属性を定義することもできます。これらのプレースホルダーは、配列を `trans_choice` 関数の 3 番目の引数として渡すことで置き換えることができます。

    'minutes_ago' => '{1} :value minute ago|[2,*] :value minutes ago',

    echo trans_choice('time.minutes_ago', 5, ['value' => 5]);

`trans_choice` 関数に渡された整数値を表示したい場合は、組み込みの `:count` プレースホルダーを使用できます。

    'apples' => '{0} There are none|{1} There is one|[2,*] There are :count',

<a name="overriding-package-language-files"></a>
## パッケージ言語ファイルの上書き (Overriding Package Language Files)

一部のパッケージには独自の言語ファイルが同梱されている場合があります。パッケージのコア ファイルを変更してこれらの行を調整する代わりに、`lang/vendor/{package}/{locale}` ディレクトリにファイルを配置することでそれらをオーバーライドできます。

したがって、たとえば、`skyrim/hearthfire` という名前のパッケージの `messages.php` 内の英語翻訳文字列をオーバーライドする必要がある場合は、言語ファイルを `lang/vendor/hearthfire/en/messages.php` に配置する必要があります。このファイル内では、オーバーライドする翻訳文字列のみを定義する必要があります。オーバーライドしない翻訳文字列は、パッケージの元の言語ファイルから読み込まれます。

