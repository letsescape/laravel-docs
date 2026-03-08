# 로컬라이제이션 (Localization)

- [소개](#introduction)
    - [언어 파일 퍼블리싱](#publishing-the-language-files)
    - [로케일 설정](#configuring-the-locale)
    - [복수형 언어](#pluralization-language)
- [번역 문자열 정의](#defining-translation-strings)
    - [짧은 키 사용](#using-short-keys)
    - [번역 문자열을 키로 사용](#using-translation-strings-as-keys)
- [번역 문자열 가져오기](#retrieving-translation-strings)
    - [번역 문자열에서 파라미터 치환](#replacing-parameters-in-translation-strings)
    - [복수형 처리](#pluralization)
- [패키지 언어 파일 오버라이드](#overriding-package-language-files)

<a name="introduction"></a>
## 소개 (Introduction)

> [!NOTE]
> 기본적으로, Laravel 애플리케이션 스캐폴드는 `lang` 디렉터리를 포함하지 않습니다. Laravel의 언어 파일을 커스터마이즈하거나 직접 만들고 싶다면, `lang:publish` Artisan 명령어를 사용해 퍼블리싱할 수 있습니다.

Laravel의 로컬라이제이션(localization) 기능은 다양한 언어의 문자열을 쉽게 가져올 수 있는 편리한 방법을 제공합니다. 이를 통해 애플리케이션에서 여러 언어를 손쉽게 지원할 수 있습니다.

Laravel에서는 번역 문자열을 관리하는 두 가지 방법을 제공합니다. 첫 번째는, 애플리케이션의 `lang` 디렉터리 내에 파일로 번역 문자열을 저장하는 방식입니다. 이 디렉터리에는 애플리케이션에서 지원하는 각 언어별로 하위 디렉터리가 있을 수 있습니다. 이 방식은 Laravel이 기본 제공 기능(예를 들면 유효성 검증 오류 메시지 등)의 번역 문자열을 관리할 때 사용하는 방법입니다:

```text
/lang
    /en
        messages.php
    /es
        messages.php
```

또는, 번역 문자열을 `lang` 디렉터리 내에 위치한 JSON 파일로 정의할 수도 있습니다. 이 방법의 경우, 지원하는 각 언어마다 해당 언어에 해당하는 JSON 파일을 이 디렉터리에 두게 됩니다. 번역해야 할 문자열이 많은 애플리케이션에서는 이 방식이 권장됩니다:

```text
/lang
    en.json
    es.json
```

이 문서에서는 번역 문자열을 관리하는 각 방식을 하나씩 설명합니다.

<a name="publishing-the-language-files"></a>
### 언어 파일 퍼블리싱 (Publishing the Language Files)

기본적으로, Laravel 애플리케이션 스캐폴드에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 커스터마이즈하거나 직접 만들고 싶다면, `lang:publish` Artisan 명령어를 사용하여 `lang` 디렉터리를 만들고, Laravel이 사용하는 기본 언어 파일 세트를 퍼블리싱해야 합니다:

```shell
php artisan lang:publish
```

<a name="configuring-the-locale"></a>
### 로케일 설정 (Configuring the Locale)

애플리케이션의 기본 언어는 `config/app.php` 설정 파일의 `locale` 설정 옵션에 저장됩니다. 보통 이 값은 `APP_LOCALE` 환경 변수로 지정되어 있습니다. 애플리케이션에 필요한 값으로 자유롭게 수정할 수 있습니다.

또한, "폴백 언어(fallback language)"도 설정할 수 있습니다. 폴백 언어는 기본 언어에 특정 번역 문자열이 없을 때 사용됩니다. 기본 언어와 마찬가지로, 폴백 언어 역시 `config/app.php` 설정 파일에서 지정하며, 일반적으로 `APP_FALLBACK_LOCALE` 환경 변수를 사용해 값을 설정합니다.

실행 중 특정 HTTP 요청에 한해 기본 언어를 변경하고 싶다면, `App` 파사드에서 제공하는 `setLocale` 메서드를 사용할 수 있습니다:

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
#### 현재 로케일 확인하기

현재 로케일을 확인하거나, 특정 값인지 검사하려면 `App` 파사드의 `currentLocale` 및 `isLocale` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\App;

$locale = App::currentLocale();

if (App::isLocale('en')) {
    // ...
}
```

<a name="pluralization-language"></a>
### 복수형 언어 (Pluralization Language)

<div class="code-list-no-flex-break">

Eloquent 및 프레임워크의 다른 부분에서 단수 형태의 문자열을 복수형으로 변환할 때 사용하는 Laravel의 "pluralizer"가 있습니다. 이 pluralizer가 영어 외의 다른 언어를 사용하도록 지정할 수 있습니다. 이를 위해서는 애플리케이션의 서비스 프로바이더 중 하나의 `boot` 메서드 안에서 `useLanguage` 메서드를 호출하면 됩니다. pluralizer에서 현재 지원하는 언어는 `french`, `norwegian-bokmal`, `portuguese`, `spanish`, `turkish` 입니다:

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
> pluralizer의 언어를 커스터마이즈하는 경우, 반드시 Eloquent 모델의 [테이블 명](/docs/master/eloquent#table-names)을 명시적으로 정의해야 합니다.

<a name="defining-translation-strings"></a>
## 번역 문자열 정의 (Defining Translation Strings)

<a name="using-short-keys"></a>
### 짧은 키 사용 (Using Short Keys)

일반적으로 번역 문자열은 `lang` 디렉터리 내의 파일에 저장됩니다. 이 디렉터리에는 애플리케이션에서 지원하는 각 언어별 하위 디렉터리가 있어야 합니다. 이 방식은 Laravel에서 기본 제공 기능(유효성 오류 메시지 등)의 번역 문자열을 관리하는 데 사용합니다:

```text
/lang
    /en
        messages.php
    /es
        messages.php
```

모든 언어 파일은 키가 지정된 문자열의 배열을 반환해야 합니다. 예시:

```php
<?php

// lang/en/messages.php

return [
    'welcome' => 'Welcome to our application!',
];
```

> [!WARNING]
> 국가마다 달라지는 언어의 경우, 언어 디렉터리 이름은 ISO 15897 규격에 따라 지어야 합니다. 예를 들어, 영국 영어는 "en-gb" 대신 "en_GB"로 지정해야 합니다.

<a name="using-translation-strings-as-keys"></a>
### 번역 문자열을 키로 사용 (Using Translation Strings as Keys)

번역해야 할 문자열이 매우 많은 애플리케이션에서는, 모든 문자열에 일일이 "짧은 키"를 붙이는 것이 번거롭고, 뷰에서 키를 참조하기가 어려워질 수 있습니다.

이러한 점을 해결하기 위해, Laravel에서는 문자열의 "기본 번역" 자체를 키로 사용하는 방식도 지원합니다. 번역 문자열을 키로 사용하는 언어 파일은 `lang` 디렉터리에 JSON 파일로 저장됩니다. 예를 들어, 스페인어 번역이 필요하다면 `lang/es.json` 파일을 생성해야 합니다:

```json
{
    "I love programming.": "Me encanta programar."
}
```

#### 키 / 파일 충돌 주의

다른 번역 파일명과 충돌하는 키는 정의하지 않는 것이 좋습니다. 예를 들어, "NL" 로케일에서 `__('Action')`을 번역하려고 할 때 `nl/action.php` 파일은 존재하지만, `nl.json` 파일이 없다면, 번역기는 `nl/action.php`의 모든 내용을 반환하게 됩니다.

<a name="retrieving-translation-strings"></a>
## 번역 문자열 가져오기 (Retrieving Translation Strings)

`__` 헬퍼 함수를 사용하여 번역 문자열을 언어 파일에서 가져올 수 있습니다. "짧은 키"를 사용하는 경우에는, 키가 포함된 파일명과 키 자체를 "점(.)" 문법으로 `__`에 전달합니다. 예를 들어, `lang/en/messages.php` 파일의 `welcome` 번역 문자열을 가져오려면 다음과 같이 할 수 있습니다:

```php
echo __('messages.welcome');
```

지정한 번역 문자열이 존재하지 않으면, `__` 함수는 번역 문자열 키 자체를 반환합니다. 위 예시에서 번역 문자열이 없으면 `messages.welcome`이 반환됩니다.

[기본 번역 문자열을 키로 사용하는 방식](#using-translation-strings-as-keys)을 사용하는 경우에는, 해당 문자열의 기본 번역값을 그대로 `__` 함수에 전달하면 됩니다:

```php
echo __('I love programming.');
```

이 또한 번역 문자열이 없으면, 전달된 번역 문자열 키 값이 그대로 반환됩니다.

[Blade 템플릿 엔진](/docs/master/blade)을 사용할 때는, `{{ }}` 이코(echo) 문법을 사용해 번역 문자열을 표시할 수 있습니다:

```blade
{{ __('messages.welcome') }}
```

<a name="replacing-parameters-in-translation-strings"></a>
### 번역 문자열에서 파라미터 치환 (Replacing Parameters in Translation Strings)

필요하다면 번역 문자열에 플레이스홀더를 정의할 수 있습니다. 모든 플레이스홀더는 `:`로 시작합니다. 예를 들어, 이름을 넣는 환영 메시지는 다음과 같이 만들 수 있습니다:

```php
'welcome' => 'Welcome, :name',
```

번역 문자열에서 플레이스홀더를 치환하려면, `__` 함수의 두 번째 인자로 치환할 값을 담은 배열을 전달합니다:

```php
echo __('messages.welcome', ['name' => 'dayle']);
```

플레이스홀더가 모두 대문자거나, 첫 글자만 대문자인 경우에는, 치환된 값도 이에 맞춰 대소문자가 적용됩니다:

```php
'welcome' => 'Welcome, :NAME', // Welcome, DAYLE
'goodbye' => 'Goodbye, :Name', // Goodbye, Dayle
```

<a name="object-replacement-formatting"></a>
#### 객체 치환 포맷팅

만약 플레이스홀더 값으로 객체를 전달한다면, 객체의 `__toString` 메서드가 호출됩니다. [__toString](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) 메서드는 PHP에 내장된 "매직 메서드" 중 하나입니다. 그러나 경우에 따라 해당 클래스가 서드파티 라이브러리에 속해있어서, `__toString` 메서드를 직접 제어할 수 없을 때도 있습니다.

이런 경우에는, 해당 객체 타입의 값을 변환하는 핸들러를 직접 등록할 수 있습니다. 이를 위해 번역기의 `stringable` 메서드를 사용합니다. `stringable` 메서드는 변환 대상 객체 타입을 타입힌트로 받는 클로저를 인자로 받습니다. 보통, 이 메서드는 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출해야 합니다:

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
### 복수형 처리 (Pluralization)

복수형 처리는 언어에 따라 복잡한 규칙을 가지고 있습니다. 하지만 Laravel은 여러분이 정의하는 복수형 규칙에 따라 번역 문자열을 다르게 변환할 수 있습니다. 문자열 내에 `|` 문자로 단수와 복수의 형태를 구분하여 작성할 수 있습니다:

```php
'apples' => 'There is one apple|There are many apples',
```

물론, [번역 문자열을 키로 사용할 때](#using-translation-strings-as-keys)도 복수형 처리를 지원합니다:

```json
{
    "There is one apple|There are many apples": "Hay una manzana|Hay muchas manzanas"
}
```

값의 범위에 따라 여러 형태의 복수형도 지정할 수 있습니다:

```php
'apples' => '{0} There are none|[1,19] There are some|[20,*] There are many',
```

이렇게 복수형 옵션이 있는 번역 문자열을 정의한 뒤에는, `trans_choice` 함수를 사용해서 주어진 "count" 값에 해당하는 번역 문자열을 가져올 수 있습니다. 아래 예시처럼 count가 1보다 크면 복수형이 반환됩니다:

```php
echo trans_choice('messages.apples', 10);
```

복수형 번역 문자열에도 플레이스홀더 속성을 추가할 수 있습니다. 플레이스홀더 치환은 배열을 `trans_choice` 함수의 세 번째 인자로 전달하여 처리합니다:

```php
'minutes_ago' => '{1} :value minute ago|[2,*] :value minutes ago',

echo trans_choice('time.minutes_ago', 5, ['value' => 5]);
```

넘긴 정수 값을 번역 문자열에 그대로 표시하고 싶다면, 내장된 `:count` 플레이스홀더를 사용할 수도 있습니다:

```php
'apples' => '{0} There are none|{1} There is one|[2,*] There are :count',
```

<a name="overriding-package-language-files"></a>
## 패키지 언어 파일 오버라이드 (Overriding Package Language Files)

일부 패키지는 자체적으로 언어 파일을 제공합니다. 이러한 문자열을 수정하려고 패키지의 핵심 파일을 직접 변경하는 대신, `lang/vendor/{package}/{locale}` 디렉터리에 파일을 두면 오버라이드할 수 있습니다.

예를 들어, 패키지명이 `skyrim/hearthfire`이고 영어 번역 파일(messages.php)을 오버라이드하려면, `lang/vendor/hearthfire/en/messages.php`에 언어 파일을 두면 됩니다. 이 파일에는 오버라이드하려는 번역 문자열만 정의하면 되며, 오버라이드하지 않은 문자열은 패키지의 원래 언어 파일에서 불러옵니다.
