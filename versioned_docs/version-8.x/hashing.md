<!-- # Hashing -->
# Hashing

- [Introduction](#introduction)
- [Configuration](#configuration)
- [Basic Usage](#basic-usage)
    - [Hashing Passwords](#hashing-passwords)
    - [Verifying That A Password Matches A Hash](#verifying-that-a-password-matches-a-hash)
    - [Determining If A Password Needs To Be Rehashed](#determining-if-a-password-needs-to-be-rehashed)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- The Laravel `Hash` [facade](/docs/8.x/facades) provides secure Bcrypt and Argon2 hashing for storing user passwords. If you are using one of the [Laravel application starter kits](/docs/8.x/starter-kits), Bcrypt will be used for registration and authentication by default. -->
Laravel의 `Hash` [facade](/docs/8.x/facades)는 사용자 비밀번호를 안전하게 저장하기 위해 Bcrypt와 Argon2 해싱 방식을 제공합니다. [Laravel application starter kits](/docs/8.x/starter-kits) 중 하나를 사용한다면, 기본적으로 회원가입과 인증 과정에 Bcrypt가 사용됩니다.

<!-- Bcrypt is a great choice for hashing passwords because its "work factor" is adjustable, which means that the time it takes to generate a hash can be increased as hardware power increases. When hashing passwords, slow is good. The longer an algorithm takes to hash a password, the longer it takes malicious users to generate "rainbow tables" of all possible string hash values that may be used in brute force attacks against applications. -->
Bcrypt는 비밀번호 해싱을 위한 훌륭한 선택인데, 해싱에 소요되는 "워크 팩터(work factor, 연산 횟수)"를 조절할 수 있기 때문입니다. 즉, 하드웨어 성능이 높아지면 해시 생성 시간이 더 오래 걸리도록 조정할 수 있습니다. 비밀번호 해싱에 있어서는 느릴수록 좋습니다. 알고리즘이 비밀번호를 해시하는 데 오래 걸릴수록, 악의적인 사용자가 무차별 대입 공격(브루트 포스)에 쓸 수 있는 "레인보우 테이블"(모든 가능한 문자열의 해시값 목록)을 생성하는 데도 그만큼 시간이 더 들기 때문입니다.

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- The default hashing driver for your application is configured in your application's `config/hashing.php` configuration file. There are currently several supported drivers: [Bcrypt](https://en.wikipedia.org/wiki/Bcrypt) and [Argon2](https://en.wikipedia.org/wiki/Argon2) (Argon2i and Argon2id variants). -->
애플리케이션의 기본 해싱 드라이버는 `config/hashing.php` 설정 파일에서 지정할 수 있습니다. 현재 지원되는 드라이버는 [Bcrypt](https://en.wikipedia.org/wiki/Bcrypt)와 [Argon2](https://en.wikipedia.org/wiki/Argon2) (Argon2i, Argon2id 변종 포함)입니다.

> [!NOTE]
> Argon2i 드라이버를 사용하려면 PHP 7.2.0 이상, Argon2id 드라이버를 사용하려면 PHP 7.3.0 이상이 필요합니다.

<a name="basic-usage"></a>
<!-- ## Basic Usage -->
## Basic Usage

<a name="hashing-passwords"></a>
<!-- ### Hashing Passwords -->
### Hashing Passwords

<!-- You may hash a password by calling the `make` method on the `Hash` facade: -->
`Hash` 파사드의 `make` 메서드를 사용하여 비밀번호를 해싱할 수 있습니다.

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;

class PasswordController extends Controller
{
    /**
     * Update the password for the user.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request)
    {
        // Validate the new password length...

        $request->user()->fill([
            'password' => Hash::make($request->newPassword)
        ])->save();
    }
}
```

<a name="adjusting-the-bcrypt-work-factor"></a>
<!-- #### Adjusting The Bcrypt Work Factor -->
#### Adjusting The Bcrypt Work Factor

<!-- If you are using the Bcrypt algorithm, the `make` method allows you to manage the work factor of the algorithm using the `rounds` option; however, the default work factor managed by Laravel is acceptable for most applications: -->
Bcrypt 알고리즘을 사용할 때는 `make` 메서드의 `rounds` 옵션을 통해 워크 팩터를 조정할 수 있습니다. 다만, Laravel에서 관리하는 기본 값으로도 대부분의 애플리케이션에서 충분합니다.

```
$hashed = Hash::make('password', [
    'rounds' => 12,
]);
```

<a name="adjusting-the-argon2-work-factor"></a>
<!-- #### Adjusting The Argon2 Work Factor -->
#### Adjusting The Argon2 Work Factor

<!-- If you are using the Argon2 algorithm, the `make` method allows you to manage the work factor of the algorithm using the `memory`, `time`, and `threads` options; however, the default values managed by Laravel are acceptable for most applications: -->
Argon2 알고리즘을 사용할 때는 `make` 메서드의 `memory`, `time`, `threads` 옵션을 통해 워크 팩터를 조정할 수 있습니다. 하지만, Laravel의 기본 값도 대부분의 애플리케이션에서 적합하게 설정되어 있습니다.

```
$hashed = Hash::make('password', [
    'memory' => 1024,
    'time' => 2,
    'threads' => 2,
]);
```

> [!TIP]
> 각 옵션에 대한 자세한 설명은 [official PHP documentation regarding Argon hashing](https://secure.php.net/manual/en/function.password-hash.php)를 참고하시기 바랍니다.

<a name="verifying-that-a-password-matches-a-hash"></a>
<!-- ### Verifying That A Password Matches A Hash -->
### Verifying That A Password Matches A Hash

<!-- The `check` method provided by the `Hash` facade allows you to verify that a given plain-text string corresponds to a given hash: -->
`Hash` 파사드의 `check` 메서드를 통해 입력된 평문 비밀번호가 저장된 해시와 일치하는지 검증할 수 있습니다.

```
if (Hash::check('plain-text', $hashedPassword)) {
    // The passwords match...
}
```

<a name="determining-if-a-password-needs-to-be-rehashed"></a>
<!-- ### Determining If A Password Needs To Be Rehashed -->
### Determining If A Password Needs To Be Rehashed

<!-- The `needsRehash` method provided by the `Hash` facade allows you to determine if the work factor used by the hasher has changed since the password was hashed. Some applications choose to perform this check during the application's authentication process: -->
`Hash` 파사드의 `needsRehash` 메서드를 사용하면, 비밀번호가 저장된 후 해싱 알고리즘의 워크 팩터(설정)가 변경되었는지 확인할 수 있습니다. 일부 애플리케이션에서는 인증 과정 중에 이 작업을 수행하기도 합니다.

```
if (Hash::needsRehash($hashed)) {
    $hashed = Hash::make('plain-text');
}
```