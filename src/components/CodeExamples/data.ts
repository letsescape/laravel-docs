export interface CodeBlock {
  title: string;
  language: string;
  code: string;
}

export interface CodeExample {
  id: string;
  title: string;
  description: string;
  code: CodeBlock[];
  link: {
    text: string;
    url: string;
  };
}

function block(title: string, language: string, code: string): CodeBlock {
  return {title, language, code};
}

function example(
  id: string,
  title: string,
  description: string,
  code: CodeBlock[],
  linkText: string,
  linkUrl: string,
): CodeExample {
  return {id, title, description, code, link: {text: linkText, url: linkUrl}};
}

export const codeExamples: CodeExample[] = [
  example('authentication', '인증', '라라벨은 기본적으로 간단하고 안전한 인증 시스템을 제공합니다.', [
    block('라라벨 라우트에 인증 미들웨어 추가하기', 'php', `Route::get('/profile', ProfileController::class)
    ->middleware('auth');`),
    block('Auth 패사드를 통해 인증된 사용자에 접근할 수 있습니다', 'php', `use Illuminate\\Support\\Facades\\Auth;

$user = Auth::user();`),
  ], '인증 문서 읽기', '/docs/12.x/인증'),

  example('eloquent', 'Eloquent', '라라벨의 우아한 ORM은 데이터베이스 작업을 매우 쉽게 만듭니다.', [
    block('데이터베이스 테이블을 위한 모델 정의하기', 'php', `<?php

namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Model;

class Flight extends Model
{
    // ...
}`),
    block('Eloquent를 사용하여 데이터베이스에서 레코드 가져오기', 'php', `use App\\Models\\Flight;

foreach (Flight::all() as $flight) {
    echo $flight->name;
}`),
  ], 'Eloquent 문서 읽기', '/docs/12.x/eloquent'),

  example('validation', '유효성 검사', '라라벨은 기본적으로 강력한 유효성 검사 기능을 포함합니다.', [
    block('컨트롤러에서 유효성 검사 규칙 정의하기', 'php', `public function store(Request $request)
{
    $validated = $request->validate([
        'title' => 'required|max:255',
        'content' => 'required',
        'email' => 'required|email',
    ]);
}`),
    block('뷰에서 유효성 검사 오류 처리하기', 'blade', `@if ($errors->any())
    <div class="alert alert-danger">
        <ul>
            @foreach ($errors->all() as $error)
                <li>{{ $error }}</li>
            @endforeach
        </ul>
    </div>
@endif`),
  ], '유효성 검사 문서 읽기', '/docs/12.x/유효성-검사'),

  example('testing', '테스팅', '라라벨은 테스팅을 고려하여 설계되었습니다. 사실, PHPUnit을 사용한 테스팅 지원이 기본적으로 포함되어 있습니다.', [
    block('Pest를 사용하여 테스트 작성하기', 'php', `it('can create a post', function () {
    $response = $this->post('/posts', [
        'title' => 'Test Post',
        'content' => 'This is a test post content.',
    ]);

    $response->assertStatus(302);

    $this->assertDatabaseHas('posts', [
        'title' => 'Test Post',
    ]);
});`),
    block('커맨드 라인에서 테스트 실행하기', 'bash', `php artisan test`),
  ], '테스팅 문서 읽기', '/docs/12.x/테스팅'),
];
