# 해싱 (Hashing)

- [소개](#introduction)
- [설정](#configuration)
- [기본 사용법](#basic-usage)
    - [비밀번호 해싱](#hashing-passwords)
    - [비밀번호와 해시가 일치하는지 확인](#verifying-that-a-password-matches-a-hash)
    - [비밀번호 재해싱 필요 여부 판단](#determining-if-a-password-needs-to-be-rehashed)
- [해시 알고리즘 검증](#hash-algorithm-verification)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel의 `Hash` [파사드](/docs/master/facades)는 사용자 비밀번호 저장을 위한 안전한 Bcrypt 및 Argon2 해싱 기능을 제공합니다. [Laravel 애플리케이션 스타터 키트](/docs/master/starter-kits)를 사용하는 경우, 기본적으로 회원가입과 인증 시 Bcrypt가 사용됩니다.

Bcrypt는 비밀번호를 해싱할 때 매우 적합한 선택입니다. 그 이유는 "작업 인자(work factor)"를 조정할 수 있어 하드웨어 성능이 좋아져도 해시 생성 시간을 늘릴 수 있기 때문입니다. 비밀번호를 해싱할 때는 느릴수록 좋습니다. 해시 연산에 시간이 많이 걸릴수록, 악의적인 사용자가 모든 가능한 문자열의 해시 값 목록("레인보우 테이블")을 생성해서 애플리케이션을 무차별 대입(brute force) 공격하는 데 시간이 오래 걸리기 때문입니다.

<a name="configuration"></a>
## 설정 (Configuration)

기본적으로 Laravel은 데이터를 해싱할 때 `bcrypt` 해싱 드라이버를 사용합니다. 하지만, [argon](https://en.wikipedia.org/wiki/Argon2) 및 [argon2id](https://en.wikipedia.org/wiki/Argon2)와 같은 다양한 해싱 드라이버도 지원합니다.

애플리케이션에서 사용할 해싱 드라이버는 `HASH_DRIVER` 환경 변수로 지정할 수 있습니다. 그러나 Laravel에서 제공하는 해싱 드라이버의 모든 옵션을 직접 커스터마이징하고 싶다면, `config:publish` Artisan 명령어를 통해 전체 `hashing` 설정 파일을 퍼블리시해야 합니다:

```shell
php artisan config:publish hashing
```

<a name="basic-usage"></a>
## 기본 사용법 (Basic Usage)

<a name="hashing-passwords"></a>
### 비밀번호 해싱 (Hashing Passwords)

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
     * 사용자의 비밀번호를 업데이트합니다.
     */
    public function update(Request $request): RedirectResponse
    {
        // 새로운 비밀번호 길이 유효성 검사...

        $request->user()->fill([
            'password' => Hash::make($request->newPassword)
        ])->save();

        return redirect('/profile');
    }
}
```

<a name="adjusting-the-bcrypt-work-factor"></a>
#### Bcrypt 작업 인자(work factor) 조정

Bcrypt 알고리즘을 사용하는 경우, `make` 메서드에서 `rounds` 옵션을 활용해 알고리즘의 작업 인자(work factor)를 조정할 수 있습니다. 하지만 Laravel이 관리하는 기본 작업 인자 값도 대부분의 애플리케이션에 충분합니다:

```php
$hashed = Hash::make('password', [
    'rounds' => 12,
]);
```

<a name="adjusting-the-argon2-work-factor"></a>
#### Argon2 작업 인자(work factor) 조정

Argon2 알고리즘을 사용하는 경우, `make` 메서드의 `memory`, `time`, `threads` 옵션을 통해 작업 인자를 조정할 수 있습니다. 하지만 Laravel이 관리하는 기본값 역시 대부분의 경우 적절하게 설정되어 있습니다:

```php
$hashed = Hash::make('password', [
    'memory' => 1024,
    'time' => 2,
    'threads' => 2,
]);
```

> [!NOTE]
> 이러한 옵션에 대한 더 자세한 내용은 [PHP 공식 문서(Argon 해싱)](https://secure.php.net/manual/en/function.password-hash.php)를 참고하시기 바랍니다.

<a name="verifying-that-a-password-matches-a-hash"></a>
### 비밀번호와 해시가 일치하는지 확인

`Hash` 파사드가 제공하는 `check` 메서드는 주어진 평문 문자열이 지정된 해시와 일치하는지 검증할 수 있습니다:

```php
if (Hash::check('plain-text', $hashedPassword)) {
    // 비밀번호가 일치합니다...
}
```

<a name="determining-if-a-password-needs-to-be-rehashed"></a>
### 비밀번호 재해싱 필요 여부 판단

`Hash` 파사드의 `needsRehash` 메서드를 사용하면 비밀번호가 해싱된 이후 해셔에서 사용하는 작업 인자 또는 옵션이 변경되었는지 확인할 수 있습니다. 일부 애플리케이션에서는 인증 과정에서 이 검사를 수행하기도 합니다:

```php
if (Hash::needsRehash($hashed)) {
    $hashed = Hash::make('plain-text');
}
```

<a name="hash-algorithm-verification"></a>
## 해시 알고리즘 검증 (Hash Algorithm Verification)

해시 알고리즘 변경 또는 변조를 방지하기 위해, Laravel의 `Hash::check` 메서드는 먼저 주어진 해시가 애플리케이션에서 선택한 해싱 알고리즘으로 생성된 것인지 확인합니다. 만약 알고리즘이 다를 경우, `RuntimeException` 예외가 발생합니다.

대부분의 애플리케이션에서는 해싱 알고리즘이 변경되지 않으므로, 이 기능이 정상적입니다. 알고리즘이 다르면 악의적인 공격을 의미할 수 있습니다. 그러나 만약 한 알고리즘에서 다른 알고리즘으로 마이그레이션하는 등 하나의 애플리케이션에서 여러 해시 알고리즘을 지원해야 한다면, `HASH_VERIFY` 환경 변수를 `false`로 설정하여 해시 알고리즘 검증을 비활성화할 수 있습니다:

```ini
HASH_VERIFY=false
```