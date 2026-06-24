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

<!-- The Laravel `Hash` [facade](/docs/11.x/facades) provides secure Bcrypt and Argon2 hashing for storing user passwords. If you are using one of the [Laravel application starter kits](/docs/11.x/starter-kits), Bcrypt will be used for registration and authentication by default. -->
Laravel의 `Hash` [facade](/docs/11.x/facades)는 사용자 비밀번호를 저장하기 위해 안전한 Bcrypt 및 Argon2 해싱 기능을 제공합니다. [Laravel application starter kits](/docs/11.x/starter-kits) 중 하나를 사용한다면, 회원가입 및 인증에서는 기본적으로 Bcrypt가 사용됩니다.

<!-- Bcrypt is a great choice for hashing passwords because its "work factor" is adjustable, which means that the time it takes to generate a hash can be increased as hardware power increases. When hashing passwords, slow is good. The longer an algorithm takes to hash a password, the longer it takes malicious users to generate "rainbow tables" of all possible string hash values that may be used in brute force attacks against applications. -->
Bcrypt는 "work factor"(작업 강도)를 조정할 수 있기 때문에 비밀번호 해싱에 적합한 선택입니다. 이는 하드웨어 성능이 높아질수록 해시 생성에 소요되는 시간을 늘릴 수 있음을 의미합니다. 비밀번호를 해싱할 때는 느릴수록 좋습니다. 해시를 생성하는 데 시간이 오래 걸릴수록, 공격자가 모든 가능한 문자열 해시 값을 미리 계산해 두는 이른바 '레인보우 테이블'을 만드는 데 드는 시간도 함께 늘어나기 때문에, 애플리케이션에 대한 무차별 대입 공격을 방지하는 데 더 효과적입니다.

<a name="configuration"></a>
<!-- ## Configuration -->
## Configuration

<!-- By default, Laravel uses the `bcrypt` hashing driver when hashing data. However, several other hashing drivers are supported, including [`argon`](https://en.wikipedia.org/wiki/Argon2) and [`argon2id`](https://en.wikipedia.org/wiki/Argon2). -->
기본적으로 Laravel은 데이터를 해싱할 때 `bcrypt` 해싱 드라이버를 사용합니다. 그러나 [`argon`](https://en.wikipedia.org/wiki/Argon2) 및 [`argon2id`](https://en.wikipedia.org/wiki/Argon2) 등 다른 해싱 드라이버도 지원합니다.

<!-- You may specify your application's hashing driver using the `HASH_DRIVER` environment variable. But, if you want to customize all of Laravel's hashing driver options, you should publish the complete `hashing` configuration file using the `config:publish` Artisan command: -->
애플리케이션의 해싱 드라이버는 `HASH_DRIVER` 환경 변수로 지정할 수 있습니다. 그러나 Laravel의 해싱 드라이버 옵션 전체를 직접 커스터마이즈하려면, 아래의 `config:publish` Artisan 명령어를 사용해서 전체 `hashing` 설정 파일을 게시해야 합니다.

```bash
php artisan config:publish hashing
```

<a name="basic-usage"></a>
<!-- ## Basic Usage -->
## Basic Usage

<a name="hashing-passwords"></a>
<!-- ### Hashing Passwords -->
### Hashing Passwords

<!-- You may hash a password by calling the `make` method on the `Hash` facade: -->
`Hash` 파사드의 `make` 메서드를 호출하여 비밀번호를 해싱할 수 있습니다.

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
Bcrypt 알고리즘을 사용할 때는, `make` 메서드에 `rounds` 옵션을 지정하여 알고리즘의 작업 강도를 조절할 수 있습니다. 하지만 Laravel이 관리하는 기본 작업 강도 설정(디폴트 값)도 대부분의 애플리케이션에 충분합니다.

```
$hashed = Hash::make('password', [
    'rounds' => 12,
]);
```

<a name="adjusting-the-argon2-work-factor"></a>
<!-- #### Adjusting The Argon2 Work Factor -->
#### Adjusting The Argon2 Work Factor

<!-- If you are using the Argon2 algorithm, the `make` method allows you to manage the work factor of the algorithm using the `memory`, `time`, and `threads` options; however, the default values managed by Laravel are acceptable for most applications: -->
Argon2 알고리즘을 사용할 때는, `make` 메서드에 `memory`, `time`, `threads` 옵션을 지정하여 작업 강도를 조정할 수 있습니다. 하지만 Laravel이 제공하는 기본 값도 대다수의 애플리케이션에 적합합니다.

```
$hashed = Hash::make('password', [
    'memory' => 1024,
    'time' => 2,
    'threads' => 2,
]);
```

> [!NOTE]
> 각 옵션에 대한 자세한 설명은 [official PHP documentation regarding Argon hashing](https://secure.php.net/manual/en/function.password-hash.php)를 참고해 주세요.

<a name="verifying-that-a-password-matches-a-hash"></a>
<!-- ### Verifying That a Password Matches a Hash -->
### Verifying That a Password Matches a Hash

<!-- The `check` method provided by the `Hash` facade allows you to verify that a given plain-text string corresponds to a given hash: -->
`Hash` 파사드가 제공하는 `check` 메서드를 사용해, 주어진 평문 문자열이 해시와 일치하는지 확인할 수 있습니다.

```
if (Hash::check('plain-text', $hashedPassword)) {
    // The passwords match...
}
```

<a name="determining-if-a-password-needs-to-be-rehashed"></a>
<!-- ### Determining if a Password Needs to be Rehashed -->
### Determining if a Password Needs to be Rehashed

<!-- The `needsRehash` method provided by the `Hash` facade allows you to determine if the work factor used by the hasher has changed since the password was hashed. Some applications choose to perform this check during the application's authentication process: -->
`Hash` 파사드의 `needsRehash` 메서드를 통해, 기존 비밀번호 해시가 생성된 이후 해싱에 사용된 작업 강도(설정 값)가 변경되었는지를 판별할 수 있습니다. 일부 애플리케이션에서는 이러한 여부를 인증 과정에서 확인한 후, 필요할 경우 해시를 재생성하기도 합니다.

```
if (Hash::needsRehash($hashed)) {
    $hashed = Hash::make('plain-text');
}
```

<a name="hash-algorithm-verification"></a>
<!-- ## Hash Algorithm Verification -->
## Hash Algorithm Verification

<!-- To prevent hash algorithm manipulation, Laravel's `Hash::check` method will first verify the given hash was generated using the application's selected hashing algorithm. If the algorithms are different, a `RuntimeException` exception will be thrown. -->
해시 알고리즘이 조작되는 것을 방지하기 위해, Laravel의 `Hash::check` 메서드는 전달된 해시가 애플리케이션에서 선택한 해싱 알고리즘으로 생성되었는지 먼저 확인합니다. 만약 알고리즘이 다를 경우, `RuntimeException` 예외가 발생합니다.

<!-- This is the expected behavior for most applications, where the hashing algorithm is not expected to change and different algorithms can be an indication of a malicious attack. However, if you need to support multiple hashing algorithms within your application, such as when migrating from one algorithm to another, you can disable hash algorithm verification by setting the `HASH_VERIFY` environment variable to `false`: -->
이런 방식은 해싱 알고리즘이 변경되지 않는 대부분의 애플리케이션에서는 당연한 동작이며, 서로 다른 알고리즘의 혼용은 악의적인 공격의 신호가 될 수 있습니다. 그러나 한 알고리즘에서 다른 알고리즘으로 마이그레이션하는 등, 여러 해싱 알고리즘을 동시에 지원해야 하는 경우도 있을 수 있습니다. 이럴 때는 `HASH_VERIFY` 환경 변수를 `false`로 설정하여 해시 알고리즘 검증을 비활성화할 수 있습니다.

```ini
HASH_VERIFY=false
```
