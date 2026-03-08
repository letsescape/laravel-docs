# 암호화 (Encryption)

- [소개](#introduction)
- [설정](#configuration)
    - [암호화 키 점진적 교체](#gracefully-rotating-encryption-keys)
- [암호화기 사용법](#using-the-encrypter)

<a name="introduction"></a>
## 소개

Laravel의 암호화 서비스는 AES-256과 AES-128 암호화를 사용하는 OpenSSL을 통해 텍스트를 암호화하고 복호화하는 간단하고 편리한 인터페이스를 제공합니다. Laravel의 모든 암호화 값은 메시지 인증 코드(MAC)로 서명되어 암호화된 후에는 값이 변경되거나 변조되는 것을 방지합니다.

<a name="configuration"></a>
## 설정

Laravel의 암호화기를 사용하기 전에 `config/app.php` 설정 파일에서 `key` 옵션을 반드시 설정해야 합니다. 이 설정값은 `APP_KEY` 환경 변수에 의해 결정됩니다. `php artisan key:generate` 명령어를 사용해 이 변수를 생성해야 하는데, 이 명령어는 PHP의 보안 난수 생성기를 활용해 애플리케이션에 안전한 암호화 키를 만들어줍니다. 일반적으로 `APP_KEY` 환경 변수 값은 [Laravel 설치 과정](/docs/master/installation)에서 자동으로 생성됩니다.

<a name="gracefully-rotating-encryption-keys"></a>
### 암호화 키 점진적 교체

애플리케이션의 암호화 키를 교체하면 모든 인증된 사용자 세션이 로그아웃 처리됩니다. 이는 Laravel이 모든 쿠키, 특히 세션 쿠키를 암호화하기 때문입니다. 또한 이전 암호화 키로 암호화된 데이터는 복호화가 불가능해집니다.

이 문제를 완화하기 위해, Laravel은 이전 암호화 키들을 `APP_PREVIOUS_KEYS` 환경 변수에 콤마로 구분된 목록으로 입력할 수 있도록 지원합니다:

```ini
APP_KEY="base64:J63qRTDLub5NuZvP+kb8YIorGS6qFYHKVo6u7179stY="
APP_PREVIOUS_KEYS="base64:2nLsGFGzyoae2ax3EF2Lyq/hH6QghBGLIq5uL+Gp8/w="
```

이 환경 변수를 설정하면, Laravel은 암호화할 때 항상 "현재" 암호화 키를 사용합니다. 하지만 복호화할 때는 먼저 현재 키를 시도하며, 실패하면 이전 키들을 순차적으로 시도하여 어떤 키로든 복호화가 가능한 경우 성공시킵니다.

이 방식은 암호화 키 교체 시에도 사용자가 애플리케이션을 중단 없이 계속 사용할 수 있도록 합니다.

<a name="using-the-encrypter"></a>
## 암호화기 사용법

<a name="encrypting-a-value"></a>
#### 값 암호화

`Crypt` 파사드의 `encryptString` 메서드를 사용해 값을 암호화할 수 있습니다. 모든 암호화 값은 OpenSSL과 AES-256-CBC 암호 방식을 사용합니다. 또한 모두 메시지 인증 코드(MAC)로 서명되어 있어, 악의적인 사용자가 값을 변조한 경우 복호화가 자동으로 차단됩니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Crypt;

class DigitalOceanTokenController extends Controller
{
    /**
     * Store a DigitalOcean API token for the user.
     */
    public function store(Request $request): RedirectResponse
    {
        $request->user()->fill([
            'token' => Crypt::encryptString($request->token),
        ])->save();

        return redirect('/secrets');
    }
}
```

<a name="decrypting-a-value"></a>
#### 값 복호화

`Crypt` 파사드의 `decryptString` 메서드를 사용해 암호화된 값을 복호화할 수 있습니다. 만약 메시지 인증 코드가 유효하지 않거나 복호화가 실패하면 `Illuminate\Contracts\Encryption\DecryptException` 예외가 발생합니다:

```php
use Illuminate\Contracts\Encryption\DecryptException;
use Illuminate\Support\Facades\Crypt;

try {
    $decrypted = Crypt::decryptString($encryptedValue);
} catch (DecryptException $e) {
    // ...
}
```