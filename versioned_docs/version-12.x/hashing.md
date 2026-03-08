# 해싱 (Hashing)

- [소개](#introduction)
- [설정](#configuration)
- [기본 사용법](#basic-usage)
    - [비밀번호 해싱](#hashing-passwords)
    - [비밀번호가 해시와 일치하는지 검증하기](#verifying-that-a-password-matches-a-hash)
    - [비밀번호를 재해싱해야 하는지 판단하기](#determining-if-a-password-needs-to-be-rehashed)
- [해시 알고리즘 검증](#hash-algorithm-verification)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel `Hash` [파사드](/docs/12.x/facades)는 사용자 비밀번호 저장을 위한 안전한 Bcrypt와 Argon2 해싱을 제공합니다. [Laravel 애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 사용하는 경우, 기본적으로 가입 및 인증 시 Bcrypt가 사용됩니다.

Bcrypt는 "작업 계수(work factor)"를 조정할 수 있기 때문에 비밀번호 해싱에 매우 적합합니다. 작업 계수는 해시 생성에 걸리는 시간을 의미하며, 하드웨어 성능이 향상됨에 따라 이 시간을 늘릴 수 있습니다. 비밀번호 해싱에서는 느린 것이 오히려 좋습니다. 알고리즘이 비밀번호 해싱에 오래 걸릴수록 악의적인 사용자가 모든 가능한 문자열 해시 값을 포함하는 "레인보우 테이블(rainbow table)"을 생성하는 데 걸리는 시간도 길어지기 때문이며, 이는 무차별 대입 공격 방어에 유리합니다.

<a name="configuration"></a>
## 설정 (Configuration)

기본적으로 Laravel은 데이터를 해싱할 때 `bcrypt` 해싱 드라이버를 사용합니다. 다만, [argon](https://en.wikipedia.org/wiki/Argon2)과 [argon2id](https://en.wikipedia.org/wiki/Argon2) 등 다른 여러 해싱 드라이버도 지원합니다.

애플리케이션의 해싱 드라이버는 `HASH_DRIVER` 환경 변수로 지정할 수 있습니다. 하지만 Laravel의 해싱 드라이버 설정을 모두 커스터마이징하려면, `config:publish` Artisan 명령어를 사용해 전체 `hashing` 설정 파일을 퍼블리시하는 것이 좋습니다:

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
     * 사용자 비밀번호를 업데이트합니다.
     */
    public function update(Request $request): RedirectResponse
    {
        // 새 비밀번호 길이 검증...

        $request->user()->fill([
            'password' => Hash::make($request->newPassword)
        ])->save();

        return redirect('/profile');
    }
}
```

<a name="adjusting-the-bcrypt-work-factor"></a>
#### Bcrypt 작업 계수 조정하기

Bcrypt 알고리즘을 사용하는 경우, `make` 메서드에서 `rounds` 옵션을 통해 작업 계수를 조정할 수 있습니다. 하지만 Laravel에서 기본으로 관리하는 작업 계수는 대부분의 애플리케이션에 적합합니다:

```php
$hashed = Hash::make('password', [
    'rounds' => 12,
]);
```

<a name="adjusting-the-argon2-work-factor"></a>
#### Argon2 작업 계수 조정하기

Argon2 알고리즘을 사용하는 경우, `make` 메서드에서 `memory`, `time`, `threads` 옵션으로 작업 계수를 조정할 수 있습니다. 그러나 Laravel에서 기본으로 관리하는 값도 대부분의 상황에 적합합니다:

```php
$hashed = Hash::make('password', [
    'memory' => 1024,
    'time' => 2,
    'threads' => 2,
]);
```

> [!NOTE]
> 이 옵션들에 대한 자세한 내용은 [PHP 공식 문서의 Argon 해싱 관련 부분](https://secure.php.net/manual/en/function.password-hash.php)을 참고하세요.

<a name="verifying-that-a-password-matches-a-hash"></a>
### 비밀번호가 해시와 일치하는지 검증하기 (Verifying That a Password Matches a Hash)

`Hash` 파사드의 `check` 메서드를 사용하면, 특정 평문 문자열이 주어진 해시와 일치하는지 검증할 수 있습니다:

```php
if (Hash::check('plain-text', $hashedPassword)) {
    // 비밀번호가 일치합니다...
}
```

<a name="determining-if-a-password-needs-to-be-rehashed"></a>
### 비밀번호를 재해싱해야 하는지 판단하기 (Determining if a Password Needs to be Rehashed)

`Hash` 파사드의 `needsRehash` 메서드를 통해, 비밀번호가 해싱되었을 때 사용된 작업 계수가 변경되었는지 확인할 수 있습니다. 일부 애플리케이션에서는 인증 과정 중에 이 검사를 수행하기도 합니다:

```php
if (Hash::needsRehash($hashed)) {
    $hashed = Hash::make('plain-text');
}
```

<a name="hash-algorithm-verification"></a>
## 해시 알고리즘 검증 (Hash Algorithm Verification)

해시 알고리즘 변조를 방지하기 위해, Laravel의 `Hash::check` 메서드는 입력된 해시가 애플리케이션에서 선택한 해싱 알고리즘으로 생성되었는지 우선 확인합니다. 알고리즘이 다르면 `RuntimeException` 예외가 발생합니다.

이는 대부분 해싱 알고리즘이 변경되지 않을 것을 기대하는 애플리케이션에서 정상적인 동작이며, 다른 알고리즘은 악의적인 공격의 가능성을 나타낼 수 있습니다. 다만, 알고리즘을 이전하면서 여러 해싱 알고리즘을 지원해야 하는 경우 `HASH_VERIFY` 환경 변수를 `false`로 설정해 해시 알고리즘 검증을 비활성화할 수 있습니다:

```ini
HASH_VERIFY=false
```