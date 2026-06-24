<!-- # Hashing -->
# Hashing

- [Introduction](#introduction)
- [Configuration](#configuration)
- [Basic Usage](#basic-usage)
    - [Hashing Passwords](#hashing-passwords)
    - [Verifying That a Password Matches a Hash](#verifying-that-a-password-matches-a-hash)
    - [Determining if a Password Needs to be Rehashed](#determining-if-a-password-needs-to-be-rehashed)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- The Laravel `Hash` [facade](/docs/10.x/facades) provides secure Bcrypt and Argon2 hashing for storing user passwords. If you are using one of the [Laravel application starter kits](/docs/10.x/starter-kits), Bcrypt will be used for registration and authentication by default. -->
Laravel의 `Hash` [facade](/docs/10.x/facades)는 사용자의 비밀번호를 안전하게 저장할 수 있도록 Bcrypt와 Argon2 해싱 기능을 제공합니다. [Laravel application starter kits](/docs/10.x/starter-kits) 중 하나를 사용하고 있다면, 기본적으로 Bcrypt가 회원가입과 인증 과정에 사용됩니다.

<!-- Bcrypt is a great choice for hashing passwords because its "work factor" is adjustable, which means that the time it takes to generate a hash can be increased as hardware power increases. When hashing passwords, slow is good. The longer an algorithm takes to hash a password, the longer it takes malicious users to generate "rainbow tables" of all possible string hash values that may be used in brute force attacks against applications. -->
Bcrypt는 비밀번호를 해싱하는 데 있어서 매우 적합한 선택입니다. 그 이유는 "워크 팩터(work factor)"를 조절할 수 있기 때문입니다. 워크 팩터는 해시를 생성하는 데 걸리는 시간을 의미하며, 하드웨어 성능이 향상됨에 따라 이 값을 증가시켜 보안을 강화할 수 있습니다. 비밀번호를 해싱할 때는 속도가 느릴수록 오히려 좋습니다. 해시 생성에 시간이 많이 걸릴수록, 악의적인 사용자가 가능한 모든 문자열 해시 값을 미리 생성해 두는 "레인보우 테이블"을 만드는 데 시간이 더 많이 걸리기 때문에, 무차별 대입 공격에 강해집니다.

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- The default hashing driver for your application is configured in your application's `config/hashing.php` configuration file. There are currently several supported drivers: [Bcrypt](https://en.wikipedia.org/wiki/Bcrypt) and [Argon2](https://en.wikipedia.org/wiki/Argon2) (Argon2i and Argon2id variants). -->
애플리케이션에서 사용할 기본 해싱 드라이버는 `config/hashing.php` 설정 파일에서 지정할 수 있습니다. 현재 지원되는 드라이버는 [Bcrypt](https://en.wikipedia.org/wiki/Bcrypt)와 [Argon2](https://en.wikipedia.org/wiki/Argon2) (Argon2i, Argon2id 변형 포함)입니다.

<a name="basic-usage"></a>
<!-- ## Basic Usage -->
## Basic Usage

<a name="hashing-passwords"></a>
<!-- ### Hashing Passwords -->
### Hashing Passwords

<!-- You may hash a password by calling the `make` method on the `Hash` facade: -->
`Hash` 파사드의 `make` 메서드를 사용해 비밀번호를 해싱할 수 있습니다.

```
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
Bcrypt 알고리즘을 사용할 경우, `make` 메서드의 `rounds` 옵션을 통해 워크 팩터를 직접 조정할 수 있습니다. 다만, Laravel에서 기본으로 제공하는 워크 팩터 값도 대부분의 애플리케이션에서 충분합니다.

```
$hashed = Hash::make('password', [
    'rounds' => 12,
]);
```

<a name="adjusting-the-argon2-work-factor"></a>
<!-- #### Adjusting The Argon2 Work Factor -->
#### Adjusting The Argon2 Work Factor

<!-- If you are using the Argon2 algorithm, the `make` method allows you to manage the work factor of the algorithm using the `memory`, `time`, and `threads` options; however, the default values managed by Laravel are acceptable for most applications: -->
Argon2 알고리즘을 사용할 경우, `make` 메서드에서 `memory`, `time`, `threads` 등의 옵션으로 워크 팩터를 조정할 수 있습니다. 이 역시 Laravel에서 관리하는 기본값이 대부분의 상황에서 적절합니다.

```
$hashed = Hash::make('password', [
    'memory' => 1024,
    'time' => 2,
    'threads' => 2,
]);
```

> [!NOTE]
> 이 옵션들에 대한 더 자세한 내용은 [official PHP documentation regarding Argon hashing](https://secure.php.net/manual/en/function.password-hash.php)를 참고하시기 바랍니다.

<a name="verifying-that-a-password-matches-a-hash"></a>
<!-- ### Verifying That a Password Matches a Hash -->
### Verifying That a Password Matches a Hash

<!-- The `check` method provided by the `Hash` facade allows you to verify that a given plain-text string corresponds to a given hash: -->
`Hash` 파사드의 `check` 메서드를 사용하면, 주어진 평문 문자열이 특정 해시 값과 일치하는지 확인할 수 있습니다.

```
if (Hash::check('plain-text', $hashedPassword)) {
    // The passwords match...
}
```

<a name="determining-if-a-password-needs-to-be-rehashed"></a>
<!-- ### Determining if a Password Needs to be Rehashed -->
### Determining if a Password Needs to be Rehashed

<!-- The `needsRehash` method provided by the `Hash` facade allows you to determine if the work factor used by the hasher has changed since the password was hashed. Some applications choose to perform this check during the application's authentication process: -->
`Hash` 파사드의 `needsRehash` 메서드를 사용하면, 기존 해시가 현재의 워크 팩터와 다른지(즉, 재해싱이 필요한지) 확인할 수 있습니다. 일부 애플리케이션에서는 인증 과정에서 이 검사를 수행하기도 합니다.

```
if (Hash::needsRehash($hashed)) {
    $hashed = Hash::make('plain-text');
}
```