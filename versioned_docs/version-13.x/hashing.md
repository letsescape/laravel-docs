<!-- # Hashing -->
# Hashing

- [Introduction](#introduction)
- [Configuration](#configuration)
- [Basic Usage](#basic-usage)
    - [Hashing Passwords](#hashing-passwords)
    - [Verifying That a Password Matches a Hash](#verifying-that-a-password-matches-a-hash)
    - [Determining if a Password Needs to be Rehashed](#determining-if-a-password-needs-to-be-rehashed)
- [Hash Algorithm Verification](#hash-algorithm-verification)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- The Laravel `Hash` [facade](/docs/13.x/facades) provides secure Bcrypt and Argon2 hashing for storing user passwords. If you are using one of the [Laravel application starter kits](/docs/13.x/starter-kits), Bcrypt will be used for registration and authentication by default. -->
Laravel `Hash` [facade](/docs/13.x/facades)는 사용자 비밀번호 저장을 위한 안전한 Bcrypt와 Argon2 해싱을 제공합니다. [Laravel application starter kits](/docs/13.x/starter-kits)를 사용하는 경우, 기본적으로 가입 및 인증 시 Bcrypt가 사용됩니다.

<!-- Bcrypt is a great choice for hashing passwords because its "work factor" is adjustable, which means that the time it takes to generate a hash can be increased as hardware power increases. When hashing passwords, slow is good. The longer an algorithm takes to hash a password, the longer it takes malicious users to generate "rainbow tables" of all possible string hash values that may be used in brute force attacks against applications. -->
Bcrypt는 "작업 계수(work factor)"를 조정할 수 있기 때문에 비밀번호 해싱에 매우 적합합니다. 작업 계수는 해시 생성에 걸리는 시간을 의미하며, 하드웨어 성능이 향상됨에 따라 이 시간을 늘릴 수 있습니다. 비밀번호 해싱에서는 느린 것이 오히려 좋습니다. 알고리즘이 비밀번호 해싱에 오래 걸릴수록 악의적인 사용자가 모든 가능한 문자열 해시 값을 포함하는 "레인보우 테이블(rainbow table)"을 생성하는 데 걸리는 시간도 길어지기 때문이며, 이는 무차별 대입 공격 방어에 유리합니다.

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- By default, Laravel uses the `bcrypt` hashing driver when hashing data. However, several other hashing drivers are supported, including [argon](https://en.wikipedia.org/wiki/Argon2) and [argon2id](https://en.wikipedia.org/wiki/Argon2). -->
기본적으로 Laravel은 데이터를 해싱할 때 `bcrypt` 해싱 드라이버를 사용합니다. 다만, [argon](https://en.wikipedia.org/wiki/Argon2)과 [argon2id](https://en.wikipedia.org/wiki/Argon2) 등 다른 여러 해싱 드라이버도 지원합니다.

<!-- You may specify your application's hashing driver using the `HASH_DRIVER` environment variable. But, if you want to customize all of Laravel's hashing driver options, you should publish the complete `hashing` configuration file using the `config:publish` Artisan command: -->
애플리케이션의 해싱 드라이버는 `HASH_DRIVER` 환경 변수로 지정할 수 있습니다. 하지만 Laravel의 해싱 드라이버 설정을 모두 사용자 지정하려면, `config:publish` Artisan 명령어를 사용해 전체 `hashing` 설정 파일을 퍼블리시하는 것이 좋습니다:

```shell
php artisan config:publish hashing
```

<a name="basic-usage"></a>
<!-- ## Basic Usage -->
## Basic Usage

<a name="hashing-passwords"></a>
<!-- ### Hashing Passwords -->
### Hashing Passwords

<!-- You may hash a password by calling the `make` method on the `Hash` facade: -->
`Hash` 파사드의 `make` 메서드를 호출하여 비밀번호를 해싱할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;

class PasswordController extends Controller
{
    /**
     * Update the password for the user.
     */
    public function update(Request $request): RedirectResponse
    {
        // Validate the new password length...

        $request->user()->fill([
            'password' => Hash::make($request->newPassword)
        ])->save();

        return redirect('/profile');
    }
}
```

<a name="adjusting-the-bcrypt-work-factor"></a>
<!-- #### Adjusting The Bcrypt Work Factor -->
#### Adjusting The Bcrypt Work Factor

<!-- If you are using the Bcrypt algorithm, the `make` method allows you to manage the work factor of the algorithm using the `rounds` option; however, the default work factor managed by Laravel is acceptable for most applications: -->
Bcrypt 알고리즘을 사용하는 경우, `make` 메서드에서 `rounds` 옵션을 통해 작업 계수를 조정할 수 있습니다. 하지만 Laravel에서 기본으로 관리하는 작업 계수는 대부분의 애플리케이션에 적합합니다:

```php
$hashed = Hash::make('password', [
    'rounds' => 12,
]);
```

<a name="adjusting-the-argon2-work-factor"></a>
<!-- #### Adjusting The Argon2 Work Factor -->
#### Adjusting The Argon2 Work Factor

<!-- If you are using the Argon2 algorithm, the `make` method allows you to manage the work factor of the algorithm using the `memory`, `time`, and `threads` options; however, the default values managed by Laravel are acceptable for most applications: -->
Argon2 알고리즘을 사용하는 경우, `make` 메서드에서 `memory`, `time`, `threads` 옵션으로 작업 계수를 조정할 수 있습니다. 그러나 Laravel에서 기본으로 관리하는 값도 대부분의 상황에 적합합니다:

```php
$hashed = Hash::make('password', [
    'memory' => 1024,
    'time' => 2,
    'threads' => 2,
]);
```

> [!NOTE]
> 이 옵션들에 대한 자세한 내용은 [official PHP documentation regarding Argon hashing](https://secure.php.net/manual/en/function.password-hash.php)을 참고하세요.

<a name="verifying-that-a-password-matches-a-hash"></a>
<!-- ### Verifying That a Password Matches a Hash -->
### Verifying That a Password Matches a Hash

<!-- The `check` method provided by the `Hash` facade allows you to verify that a given plain-text string corresponds to a given hash: -->
`Hash` 파사드의 `check` 메서드를 사용하면, 특정 평문 문자열이 주어진 해시와 일치하는지 검증할 수 있습니다:

```php
if (Hash::check('plain-text', $hashedPassword)) {
    // The passwords match...
}
```

<a name="determining-if-a-password-needs-to-be-rehashed"></a>
<!-- ### Determining if a Password Needs to be Rehashed -->
### Determining if a Password Needs to be Rehashed

<!-- The `needsRehash` method provided by the `Hash` facade allows you to determine if the work factor used by the hasher has changed since the password was hashed. Some applications choose to perform this check during the application's authentication process: -->
`Hash` 파사드의 `needsRehash` 메서드를 통해, 비밀번호가 해싱되었을 때 사용된 작업 계수가 변경되었는지 확인할 수 있습니다. 일부 애플리케이션에서는 인증 과정 중에 이 검사를 수행하기도 합니다:

```php
if (Hash::needsRehash($hashed)) {
    $hashed = Hash::make('plain-text');
}
```

<a name="hash-algorithm-verification"></a>
<!-- ## Hash Algorithm Verification -->
## Hash Algorithm Verification

<!-- To prevent hash algorithm manipulation, Laravel's `Hash::check` method will first verify the given hash was generated using the application's selected hashing algorithm. If the algorithms are different, a `RuntimeException` exception will be thrown. -->
해시 알고리즘 변조를 방지하기 위해, Laravel의 `Hash::check` 메서드는 입력된 해시가 애플리케이션에서 선택한 해싱 알고리즘으로 생성되었는지 우선 확인합니다. 알고리즘이 다르면 `RuntimeException` 예외가 발생합니다.

<!-- This is the expected behavior for most applications, where the hashing algorithm is not expected to change and different algorithms can be an indication of a malicious attack. However, if you need to support multiple hashing algorithms within your application, such as when migrating from one algorithm to another, you can disable hash algorithm verification by setting the `HASH_VERIFY` environment variable to `false`: -->
이는 대부분 해싱 알고리즘이 변경되지 않을 것을 기대하는 애플리케이션에서 정상적인 동작이며, 다른 알고리즘은 악의적인 공격의 가능성을 나타낼 수 있습니다. 다만, 알고리즘을 이전하면서 여러 해싱 알고리즘을 지원해야 하는 경우 `HASH_VERIFY` 환경 변수를 `false`로 설정해 해시 알고리즘 검증을 비활성화할 수 있습니다:

```ini
HASH_VERIFY=false
```
