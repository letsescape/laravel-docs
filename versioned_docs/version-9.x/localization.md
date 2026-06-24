<!-- # Localization -->
# Localization

- [Introduction](#introduction)
    - [Configuring The Locale](#configuring-the-locale)
    - [Pluralization Language](#pluralization-language)
- [Defining Translation Strings](#defining-translation-strings)
    - [Using Short Keys](#using-short-keys)
    - [Using Translation Strings As Keys](#using-translation-strings-as-keys)
- [Retrieving Translation Strings](#retrieving-translation-strings)
    - [Replacing Parameters In Translation Strings](#replacing-parameters-in-translation-strings)
    - [Pluralization](#pluralization)
- [Overriding Package Language Files](#overriding-package-language-files)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel's localization features provide a convenient way to retrieve strings in various languages, allowing you to easily support multiple languages within your application. -->
Laravel의 로컬라이제이션(Localization) 기능을 사용하면 다양한 언어로 문자열을 가져올 수 있어, 애플리케이션에서 여러 언어를 손쉽게 지원할 수 있습니다.

<!-- Laravel provides two ways to manage translation strings. First, language strings may be stored in files within the `lang` directory. Within this directory, there may be subdirectories for each language supported by the application. This is the approach Laravel uses to manage translation strings for built-in Laravel features such as validation error messages: -->
Laravel에서는 번역 문자열을 관리하는 두 가지 방법을 제공합니다. 첫 번째는 `lang` 디렉터리 내에 파일로 번역 문자열을 저장하는 방식입니다. 이 디렉터리 안에는 애플리케이션에서 지원하는 각 언어별로 서브디렉터리를 만들 수 있습니다. Laravel의 기본 기능(예: 유효성 검증 에러 메시지)도 이런 방법을 사용합니다.


```
/lang
    /en
        messages.php
    /es
        messages.php
```


<!-- Or, translation strings may be defined within JSON files that are placed within the `lang` directory. When taking this approach, each language supported by your application would have a corresponding JSON file within this directory. This approach is recommended for applications that have a large number of translatable strings: -->
또는, 번역 문자열을 `lang` 디렉터리 내의 JSON 파일에 정의할 수도 있습니다. 이 때는 애플리케이션에서 지원하는 각 언어마다 해당하는 JSON 파일을 이 디렉터리에 둡니다. 번역해야 할 문자열이 많은 애플리케이션에는 이 방식을 권장합니다.

```
/lang
    en.json
    es.json
```

<!-- We'll discuss each approach to managing translation strings within this documentation. -->
이 문서에서는 이 두 방식 각각에 대해 자세히 설명합니다.

<a name="configuring-the-locale"></a>
<!-- ### Configuring The Locale -->
### Configuring The Locale

<!-- The default language for your application is stored in the `config/app.php` configuration file's `locale` configuration option. You are free to modify this value to suit the needs of your application. -->
애플리케이션의 기본 언어는 `config/app.php` 설정 파일의 `locale` 옵션에 저장되어 있습니다. 애플리케이션의 필요에 따라 이 값을 자유롭게 변경할 수 있습니다.

<!-- You may modify the default language for a single HTTP request at runtime using the `setLocale` method provided by the `App` facade: -->
또한, `App` 파사드에서 제공하는 `setLocale` 메서드를 사용하면 런타임 중, 특정 HTTP 요청에 대해서 기본 언어를 변경할 수 있습니다.

```
use Illuminate\Support\Facades\App;

Route::get('/greeting/{locale}', function ($locale) {
    if (! in_array($locale, ['en', 'es', 'fr'])) {
        abort(400);
    }

    App::setLocale($locale);

    //
});
```

<!-- You may configure a "fallback language", which will be used when the active language does not contain a given translation string. Like the default language, the fallback language is also configured in the `config/app.php` configuration file: -->
"대체 언어(fallback language)"도 설정할 수 있습니다. 대체 언어는 현재 활성화된 언어에 특정 번역 문자열이 없을 때 사용됩니다. 기본 언어와 마찬가지로 `config/app.php` 설정 파일에서 지정합니다.

```
'fallback_locale' => 'en',
```

<a name="determining-the-current-locale"></a>
<!-- #### Determining The Current Locale -->
#### Determining The Current Locale

<!-- You may use the `currentLocale` and `isLocale` methods on the `App` facade to determine the current locale or check if the locale is a given value: -->
`App` 파사드의 `currentLocale` 및 `isLocale` 메서드를 사용해 현재 로케일을 확인하거나, 특정 값과 일치하는지 체크할 수 있습니다.

```
use Illuminate\Support\Facades\App;

$locale = App::currentLocale();

if (App::isLocale('en')) {
    //
}
```

<a name="pluralization-language"></a>
<!-- ### Pluralization Language -->
### Pluralization Language

<!-- You may instruct Laravel's "pluralizer", which is used by Eloquent and other portions of the framework to convert singular strings to plural strings, to use a language other than English. This may be accomplished by invoking the `useLanguage` method within the `boot` method of one of your application's service providers. The pluralizer's currently supported languages are: `french`, `norwegian-bokmal`, `portuguese`, `spanish`, and `turkish`: -->
Eloquent 등 프레임워크 내부에서는 단어를 단수에서 복수로 변환할 때 "pluralizer(복수형 변환기)"를 사용하는데, 이 언어를 영어가 아닌 다른 언어로 변경할 수 있습니다. 이를 위해 애플리케이션의 서비스 프로바이더 중 하나의 `boot` 메서드에서 `useLanguage` 메서드를 호출하세요. 현재 pluralizer가 지원하는 언어는: `french`, `norwegian-bokmal`, `portuguese`, `spanish`, `turkish`입니다.

```
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
```

> [!WARNING]
> 복수형 변환기의 언어를 커스터마이즈한 경우, Eloquent 모델의 [table names](/docs/9.x/eloquent#table-names)은 반드시 직접 명시적으로 지정해야 합니다.

<a name="defining-translation-strings"></a>
<!-- ## Defining Translation Strings -->
## Defining Translation Strings

<a name="using-short-keys"></a>
<!-- ### Using Short Keys -->
### Using Short Keys

<!-- Typically, translation strings are stored in files within the `lang` directory. Within this directory, there should be a subdirectory for each language supported by your application. This is the approach Laravel uses to manage translation strings for built-in Laravel features such as validation error messages: -->
일반적으로 번역 문자열은 `lang` 디렉터리 내의 파일에 저장합니다. 이 디렉터리에는 애플리케이션이 지원하는 각 언어별로 서브디렉터리가 있어야 합니다. Laravel의 기본 기능(예: 유효성 검증 에러 메시지)에서도 이 방식을 사용합니다.


```
/lang
    /en
        messages.php
    /es
        messages.php
```


<!-- All language files return an array of keyed strings. For example: -->
모든 언어 파일은 키가 붙은 문자열 배열을 반환해야 합니다. 예시:

```
<?php

// lang/en/messages.php

return [
    'welcome' => 'Welcome to our application!',
];
```

> [!WARNING]
> 국가·지역에 따라 구분해야 하는 언어는, 디렉터리 이름을 반드시 ISO 15897 규격에 맞춰 지정해야 합니다. 예를 들어 영국 영어는 "en-gb"가 아니라 "en_GB"로 디렉터리를 만들어야 합니다.

<a name="using-translation-strings-as-keys"></a>
<!-- ### Using Translation Strings As Keys -->
### Using Translation Strings As Keys

<!-- For applications with a large number of translatable strings, defining every string with a "short key" can become confusing when referencing the keys in your views and it is cumbersome to continually invent keys for every translation string supported by your application. -->
번역 가능 문자열이 많은 애플리케이션에서는, 모든 번역 문자열에 대해 일일이 "짧은 키"를 만들어 관리하다 보면 뷰에서 참조하기 어렵고, 키 이름을 계속 새로 만드는 작업이 번거롭게 느껴질 수 있습니다.

<!-- For this reason, Laravel also provides support for defining translation strings using the "default" translation of the string as the key. Translation files that use translation strings as keys are stored as JSON files in the `lang` directory. For example, if your application has a Spanish translation, you should create a `lang/es.json` file: -->
이런 경우를 위해, Laravel은 번역 문자열의 "기본" 텍스트 자체를 키로 사용하는 방식을 지원합니다. 이 방식의 번역 파일은 `lang` 디렉터리 내의 JSON 파일로 저장합니다. 예를 들어, 애플리케이션에 스페인어 번역이 있다면 `lang/es.json` 파일을 생성합니다.

```json
{
    "I love programming.": "Me encanta programar."
}
```

<!-- #### Key / File Conflicts -->
#### Key / File Conflicts

<!-- You should not define translation string keys that conflict with other translation filenames. For example, translating `__('Action')` for the "NL" locale while a `nl/action.php` file exists but a `nl.json` file does not exist will result in the translator returning the contents of `nl/action.php`. -->
번역 문자열의 키가 다른 번역 파일명과 충돌하지 않도록 주의해야 합니다. 예를 들어 "NL" 로케일에서 `__('Action')`을 사용했을 때, `nl/action.php` 파일이 존재하지만 `nl.json` 파일이 없다면 번역기는 `nl/action.php`의 내용을 반환합니다.

<a name="retrieving-translation-strings"></a>
<!-- ## Retrieving Translation Strings -->
## Retrieving Translation Strings

<!-- You may retrieve translation strings from your language files using the `__` helper function. If you are using "short keys" to define your translation strings, you should pass the file that contains the key and the key itself to the `__` function using "dot" syntax. For example, let's retrieve the `welcome` translation string from the `lang/en/messages.php` language file: -->
번역 문자열은 `__` 헬퍼 함수를 사용해 언어 파일에서 손쉽게 가져올 수 있습니다. "짧은 키" 방식으로 번역 문자열을 정의했다면, 해당 키가 위치한 파일명과 키를 "도트(.)" 표기법으로 묶어서 `__` 함수에 전달해야 합니다. 예를 들어, `lang/en/messages.php` 언어 파일에서 `welcome` 번역 문자열을 가져오려면 다음과 같이 사용합니다.

```
echo __('messages.welcome');
```

<!-- If the specified translation string does not exist, the `__` function will return the translation string key. So, using the example above, the `__` function would return `messages.welcome` if the translation string does not exist. -->
만약 지정한 번역 문자열이 존재하지 않을 경우, `__` 함수는 전달받은 키 자체를 그대로 반환합니다. 즉 위 예시에서 번역 문자열이 없으면 `messages.welcome`이 반환됩니다.

<!--  If you are using your [default translation strings as your translation keys](#using-translation-strings-as-keys), you should pass the default translation of your string to the `__` function; -->
[default translation strings as your translation keys](#using-translation-strings-as-keys)을 사용할 때에는, 문자열의 기본 번역값을 그대로 `__` 함수에 전달하면 됩니다.

```
echo __('I love programming.');
```

<!-- Again, if the translation string does not exist, the `__` function will return the translation string key that it was given. -->
마찬가지로, 번역 문자열이 없을 경우 `__` 함수에는 넘긴 문자열 그 자체가 반환됩니다.

<!-- If you are using the [Blade templating engine](/docs/9.x/blade), you may use the `{{ }}` echo syntax to display the translation string: -->
[Blade templating engine](/docs/9.x/blade)을 사용할 때는, `{{ }}` 구문 안에 `__` 함수를 사용해 번역 문자열을 화면에 출력할 수 있습니다.

```
{{ __('messages.welcome') }}
```

<a name="replacing-parameters-in-translation-strings"></a>
<!-- ### Replacing Parameters In Translation Strings -->
### Replacing Parameters In Translation Strings

<!-- If you wish, you may define placeholders in your translation strings. All placeholders are prefixed with a `:`. For example, you may define a welcome message with a placeholder name: -->
원하는 경우, 번역 문자열 안에 플레이스홀더(치환될 자리)를 정의할 수 있습니다. 플레이스홀더는 모두 `:`가 앞에 붙습니다. 예를 들어, 사용자 이름이 들어가는 환영 메시지에 사용할 수 있습니다.

```
'welcome' => 'Welcome, :name',
```

<!-- To replace the placeholders when retrieving a translation string, you may pass an array of replacements as the second argument to the `__` function: -->
번역 문자열에서 플레이스홀더를 실제 값으로 치환하려면, 두 번째 인자로 치환할 배열을 `__` 함수에 전달하면 됩니다.

```
echo __('messages.welcome', ['name' => 'dayle']);
```

<!-- If your placeholder contains all capital letters, or only has its first letter capitalized, the translated value will be capitalized accordingly: -->
만약 플레이스홀더 이름이 모두 대문자이거나 첫 글자만 대문자인 경우, 치환된 값도 대소문자가 맞게 표시됩니다.

```
'welcome' => 'Welcome, :NAME', // Welcome, DAYLE
'goodbye' => 'Goodbye, :Name', // Goodbye, Dayle
```

<a name="object-replacement-formatting"></a>
<!-- #### Object Replacement Formatting -->
#### Object Replacement Formatting

<!-- If you attempt to provide an object as a translation placeholder, the object's `__toString` method will be invoked. The [`__toString`](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) method is one of PHP's built-in "magic methods". However, sometimes you may not have control over the `__toString` method of a given class, such as when the class that you are interacting with belongs to a third-party library. -->
번역 문자열의 플레이스홀더에 객체를 전달하면, 객체의 `__toString` 메서드가 호출됩니다. [`__toString`](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) 메서드는 PHP에 내장된 "매직 메서드" 중 하나입니다. 하지만 타사 라이브러리에서 제공하는 클래스 등, 직접 `__toString` 메서드를 제어할 수 없는 경우도 있습니다.

<!-- In these cases, Laravel allows you to register a custom formatting handler for that particular type of object. To accomplish this, you should invoke the translator's `stringable` method. The `stringable` method accepts a closure, which should type-hint the type of object that it is responsible for formatting. Typically, the `stringable` method should be invoked within the `boot` method of your application's `AppServiceProvider` class: -->
이럴 때는, 해당 객체 타입만을 위한 커스텀 포매팅 핸들러를 등록할 수 있습니다. 이를 위해 번역기의 `stringable` 메서드를 사용하면 됩니다. `stringable` 메서드는 클로저를 받으며, 이 클로저는 포매팅을 책임질 객체의 타입을 타입힌트로 명시해야 합니다. 보통 `stringable` 메서드는 애플리케이션 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다.

```
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
```

<a name="pluralization"></a>
<!-- ### Pluralization -->
### Pluralization

<!-- Pluralization is a complex problem, as different languages have a variety of complex rules for pluralization; however, Laravel can help you translate strings differently based on pluralization rules that you define. Using a `|` character, you may distinguish singular and plural forms of a string: -->
언어마다 복수형 규칙이 복잡하게 다르기 때문에, 복수형 처리(Pluralization)는 쉽지 않은 문제입니다. 하지만 Laravel을 사용하면, 직접 정의한 복수형 규칙에 따라 번역 문자열을 다르게 표시할 수 있습니다. 문자열에서 `|` 문자로 단수와 복수 형태를 구분해서 작성할 수 있습니다.

```
'apples' => 'There is one apple|There are many apples',
```

<!-- Of course, pluralization is also supported when using [translation strings as keys](#using-translation-strings-as-keys): -->
물론, [translation strings as keys](#using-translation-strings-as-keys)에도 복수형 처리를 지원합니다.

```json
{
    "There is one apple|There are many apples": "Hay una manzana|Hay muchas manzanas"
}
```

<!-- You may even create more complex pluralization rules which specify translation strings for multiple ranges of values: -->
또한, 다음과 같이 여러 값의 구간별로 번역 문자열을 다르게 정의할 수도 있습니다.

```
'apples' => '{0} There are none|[1,19] There are some|[20,*] There are many',
```

<!-- After defining a translation string that has pluralization options, you may use the `trans_choice` function to retrieve the line for a given "count". In this example, since the count is greater than one, the plural form of the translation string is returned: -->
이처럼 복수형 옵션이 있는 번역 문자열을 만든 뒤에는, 특정 "개수"에 따라 번역 문자열을 선택할 수 있는 `trans_choice` 함수를 사용합니다. 아래 예시에서는 개수가 1보다 크므로, 복수형에 해당하는 문자열이 반환됩니다.

```
echo trans_choice('messages.apples', 10);
```

<!-- You may also define placeholder attributes in pluralization strings. These placeholders may be replaced by passing an array as the third argument to the `trans_choice` function: -->
복수형 번역 문자열에도 플레이스홀더를 추가할 수 있습니다. 이때는 `trans_choice` 함수 세 번째 인자로 배열을 전달해 치환합니다.

```
'minutes_ago' => '{1} :value minute ago|[2,*] :value minutes ago',

echo trans_choice('time.minutes_ago', 5, ['value' => 5]);
```

<!-- If you would like to display the integer value that was passed to the `trans_choice` function, you may use the built-in `:count` placeholder: -->
`trans_choice` 함수에 넘긴 숫자 값을 표시하고 싶다면, 내장된 `:count` 플레이스홀더를 활용할 수 있습니다.

```
'apples' => '{0} There are none|{1} There is one|[2,*] There are :count',
```

<a name="overriding-package-language-files"></a>
<!-- ## Overriding Package Language Files -->
## Overriding Package Language Files

<!-- Some packages may ship with their own language files. Instead of changing the package's core files to tweak these lines, you may override them by placing files in the `lang/vendor/{package}/{locale}` directory. -->
일부 패키지는 자체 언어 파일을 제공합니다. 만약 패키지의 소스 파일을 직접 수정하지 않고, 일부 번역 문자열만 수정하고 싶다면 `lang/vendor/{package}/{locale}` 디렉터리에 직접 언어 파일을 배치해 오버라이드할 수 있습니다.

<!-- So, for example, if you need to override the English translation strings in `messages.php` for a package named `skyrim/hearthfire`, you should place a language file at: `lang/vendor/hearthfire/en/messages.php`. Within this file, you should only define the translation strings you wish to override. Any translation strings you don't override will still be loaded from the package's original language files. -->
예를 들어, `skyrim/hearthfire`라는 패키지의 `messages.php` 파일에서 영어 번역 문자열을 오버라이드하고 싶다면, `lang/vendor/hearthfire/en/messages.php` 파일을 만들어 해당 파일에 원하는 번역 문자열만 정의하세요. 변경하지 않은 문자열은 패키지의 원본 언어 파일에서 계속 불러옵니다.