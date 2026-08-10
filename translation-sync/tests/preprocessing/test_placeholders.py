"""Base64 image placeholder 할당과 복원 경계 검증."""

import unittest
from unittest.mock import patch

from sync import postprocess, preprocess, verify


class PlaceholderTests(unittest.TestCase):
    """결정적 placeholder 할당과 입력별 복원표를 검증."""

    def test_pair_uses_same_placeholder_for_identical_data_uri(self):
        """같은 data URI가 이전·현재 원문에서 같은 token을 사용하는지 검증."""

        data_uri = "data:image/png;base64,QUJD"

        result = preprocess.preprocess_pair(
            f"Previous: ![x]({data_uri})\n",
            f"Current: ![x]({data_uri})\n",
        )

        self.assertEqual(
            result.previous.text,
            "Previous: ![x](__BASE64_IMAGE_001__)\n",
        )
        self.assertEqual(
            result.current.text,
            "Current: ![x](__BASE64_IMAGE_001__)\n",
        )
        self.assertEqual(
            result.previous.placeholders,
            {"__BASE64_IMAGE_001__": data_uri},
        )
        self.assertEqual(result.current.placeholders, result.previous.placeholders)

    def test_pair_allocates_union_in_sha256_digest_order(self):
        """두 입력의 합집합을 SHA-256 digest 바이트 순서로 할당."""

        result = preprocess.preprocess_pair(
            "Previous: ![jpeg](data:image/jpeg;base64,QUJD) "
            "![png](data:image/png;base64,REVG)\n",
            "Current: ![png](data:image/png;base64,QUJD)\n",
        )

        self.assertEqual(
            result.previous.text,
            "Previous: ![jpeg](__BASE64_IMAGE_003__) "
            "![png](__BASE64_IMAGE_002__)\n",
        )
        self.assertEqual(
            result.current.text,
            "Current: ![png](__BASE64_IMAGE_001__)\n",
        )

    def test_pair_allocation_is_independent_of_input_role_and_occurrence_order(self):
        """입력 역할과 출현 순서가 달라도 같은 data URI 할당을 유지."""

        first = "data:image/png;base64,QUJD"
        second = "data:image/png;base64,REVG"

        forward = preprocess.preprocess_pair(
            f"![first]({first}) ![second]({second})\n",
            f"![second]({second}) ![first]({first})\n",
        )
        reversed_pair = preprocess.preprocess_pair(
            f"![second]({second}) ![first]({first})\n",
            f"![first]({first}) ![second]({second})\n",
        )

        self.assertEqual(
            forward.previous.placeholders,
            reversed_pair.current.placeholders,
        )
        self.assertEqual(
            forward.current.placeholders,
            reversed_pair.previous.placeholders,
        )

    def test_pair_preserves_data_uris_inside_fenced_and_inline_code(self):
        """fenced code와 inline code 내부의 data URI를 보존."""

        protected = "data:image/png;base64,QUJD"
        translated = "data:image/png;base64,REVG"

        result = preprocess.preprocess_pair(
            f"Inline `{protected}`; ![x]({translated})\n",
            f"```markdown\n![x]({protected})\n```\n![x]({translated})\n",
        )

        self.assertEqual(
            result.previous.text,
            f"Inline `{protected}`; ![x](__BASE64_IMAGE_001__)\n",
        )
        self.assertEqual(
            result.current.text,
            f"```markdown\n![x]({protected})\n```\n"
            "![x](__BASE64_IMAGE_001__)\n",
        )
        self.assertEqual(
            result.current.placeholders,
            {"__BASE64_IMAGE_001__": translated},
        )

    def test_pair_preserves_data_uris_inside_multiline_inline_code(self):
        """여러 줄 inline code span 내부의 data URI를 보존."""

        protected = "data:image/png;base64,REVG"

        result = preprocess.preprocess_pair(
            f"Use ``before\n{protected}\nafter`` literally.\n",
            "",
        )

        self.assertEqual(
            result.previous.text,
            f"Use ``before\n{protected}\nafter`` literally.\n",
        )
        self.assertEqual(result.previous.placeholders, {})

    def test_pair_skips_placeholder_literals_from_either_input(self):
        """두 입력 중 하나에 존재하는 예약 token 번호와의 충돌을 회피."""

        result = preprocess.preprocess_pair(
            "Example literal: __BASE64_IMAGE_001__.\n",
            "![x](data:image/png;base64,QUJD)\n",
        )

        self.assertEqual(
            result.current.text,
            "![x](__BASE64_IMAGE_002__)\n",
        )
        self.assertEqual(
            result.current.placeholders,
            {"__BASE64_IMAGE_002__": "data:image/png;base64,QUJD"},
        )

    def test_pair_round_trips_distinct_media_types_with_the_same_payload(self):
        """payload가 같아도 media type이 다른 data URI를 별도로 복원."""

        previous = "![x](data:image/jpeg;base64,QUJD)\n"
        current = "![x](data:image/png;base64,QUJD)\n"

        result = preprocess.preprocess_pair(previous, current)

        self.assertEqual(
            result.previous.text,
            "![x](__BASE64_IMAGE_002__)\n",
        )
        self.assertEqual(
            result.current.text,
            "![x](__BASE64_IMAGE_001__)\n",
        )
        self.assertEqual(
            postprocess.postprocess(
                result.previous.text,
                "12.x",
                result.previous.placeholders,
            ),
            previous,
        )
        self.assertEqual(
            postprocess.postprocess(
                result.current.text,
                "12.x",
                result.current.placeholders,
            ),
            current,
        )

    def test_pair_rejects_sha256_digest_collision(self):
        """서로 다른 data URI의 digest가 충돌하면 fail-closed를 적용."""

        with patch.object(preprocess.hashlib, "sha256") as sha256:
            sha256.return_value.digest.return_value = b"\x00" * 32

            with self.assertRaisesRegex(ValueError, "same SHA-256 digest"):
                preprocess.preprocess_pair(
                    "![old](data:image/jpeg;base64,QUJD)\n",
                    "![new](data:image/png;base64,REVG)\n",
                )

    def test_avoids_colliding_with_literal_base64_placeholder_text(self):
        """단일 입력에 존재하는 예약 token과의 충돌을 회피."""

        source = (
            "Literal __BASE64_IMAGE_001__.\n\n"
            "![x](data:image/png;base64,QUJD)\n"
        )

        result = preprocess.preprocess(source)

        self.assertIn("__BASE64_IMAGE_002__", result.text)
        self.assertEqual(
            postprocess.postprocess(result.text, "12.x", result.placeholders),
            source,
        )

    def test_round_trips_base64_image_with_media_type_parameters(self):
        """media type parameter를 포함한 Base64 image를 복원."""

        source = "![x](data:image/svg+xml;charset=utf-8;base64,QUJD)\n"

        result = preprocess.preprocess(source)

        self.assertEqual(result.text, "![x](__BASE64_IMAGE_001__)\n")
        self.assertEqual(
            postprocess.postprocess(result.text, "12.x", result.placeholders),
            source,
        )

    def test_round_trips_base64_images_terminated_by_angle_brackets(self):
        """angle bracket로 끝나는 Markdown과 HTML data URI를 복원."""

        cases = (
            (
                "![x](<data:image/png;base64,QUJD>)\n",
                "![x](<__BASE64_IMAGE_001__>)\n",
                "![x](<data:image/png;base64,QUJD>)\n",
            ),
            (
                "<img src=data:image/png;base64,QUJD>\n",
                "<img src=__BASE64_IMAGE_001__>\n",
                "<img src=data:image/png;base64,QUJD />\n",
            ),
        )
        for source, expected_preprocessed, expected_final in cases:
            with self.subTest(source=source):
                result = preprocess.preprocess(source)

                self.assertEqual(result.text, expected_preprocessed)
                self.assertEqual(
                    postprocess.postprocess(
                        result.text, "12.x", result.placeholders
                    ),
                    expected_final,
                )

    def test_unquoted_base64_image_round_trip_passes_final_verification(self):
        """따옴표 없는 HTML data URI의 복원 결과가 최종 검증을 통과."""

        source = "<img src=data:image/png;base64,QUJD>\n"

        result = preprocess.preprocess(source)
        final = postprocess.postprocess(
            result.text,
            "12.x",
            result.placeholders,
        )

        self.assertEqual(verify.verify(final, source=source), [])

    def test_preserves_unquoted_self_closing_base64_image(self):
        """따옴표 없는 self-closing HTML data URI의 slash를 보존."""

        source = "<img src=data:image/png;base64,QQ==/>\n"

        result = preprocess.preprocess(source)
        final = postprocess.postprocess(
            result.text,
            "12.x",
            result.placeholders,
        )

        self.assertEqual(
            result.text,
            "<img src=__BASE64_IMAGE_001__/>\n",
        )
        self.assertEqual(final, source)
        self.assertEqual(verify.verify(final, source=source), [])

    def test_round_trips_base64_image_at_end_of_input(self):
        """입력 끝에서 종료되는 Base64 image data URI를 복원."""

        source = "data:image/png;base64,QUJD"

        result = preprocess.preprocess(source)

        self.assertEqual(result.text, "__BASE64_IMAGE_001__")
        self.assertEqual(
            postprocess.postprocess(result.text, "12.x", result.placeholders),
            source,
        )


if __name__ == "__main__":
    unittest.main()
