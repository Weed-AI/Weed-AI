import pathlib
import json

import pytest

from weedcoco.importers.mask import main

TEST_DATA_DIR = pathlib.Path(__file__).parent / "mask_data"
TEST_MASK_DIR = TEST_DATA_DIR / "cobbity_lbl"
TEST_IMAGE_DIR = TEST_DATA_DIR / "cobbity_img"


@pytest.fixture
def converter(tmpdir):
    out_path = tmpdir / "out.json"

    class Converter:
        def run(
            self,
            extra_args,
            mask_dir=TEST_MASK_DIR,
            image_dir=TEST_IMAGE_DIR,
            path_to_mask_pattern="....",
        ):
            args = ["--mask-dir", mask_dir, "--image-dir", image_dir, "-o", out_path]
            if path_to_mask_pattern is not None:
                args.extend(["--path-to-mask-pattern", path_to_mask_pattern])
            args.extend(extra_args)
            args = [str(arg) for arg in args]
            main(args)
            return json.load(out_path)

    return Converter()


def test_basic(converter):
    actual = converter.run(
        ["--category-map", TEST_DATA_DIR / "category_name_cobbity.yaml"]
    )
    assert len(actual["images"]) == 3
    assert len(actual["annotations"]) == 3
    # TODO: neater assertions
    expected = {
        "images": [
            {
                "id": 0,
                "file_name": "0011_20200306T012109.394627.png",
                "width": 1024,
                "height": 768,
            },
            {
                "id": 1,
                "file_name": "0054_20200306T012123.728442.png",
                "width": 1024,
                "height": 768,
            },
            {
                "id": 2,
                "file_name": "0042_20200306T012119.728345.png",
                "width": 1024,
                "height": 768,
            },
        ],
        "annotations": [
            {
                "id": 0,
                "image_id": 0,
                "category_id": 1,
                "segmentation": {
                    "size": [768, 1024],
                    "counts": "^lc66e40[>MiANX>5eAOTc0Lcf41_YK3N101NO110O01cIKnD4Q6MeHN[14n50gHMZ13m52TO0j01VOOh03kHH]15h53fHG[K2V64i53gHGZK1V65i51iHJWK1V65h51lHN[12h52lHL\\13g51nHLY14i50nHLZ13g50QINW12g50TINT11h52TIMU10f54VIKT11a58]IFR12^5:bIDo02_5:dIBl06]58jIBh06\\585HJ7oIBi07X57oIDg05[53QJJb02]54RJK`01]54UJJ>2^50XJN83`50oIHhJ5i53b5NkINiJ1i53d5MjI0iJOi54g5GiI9fJLi54X;OP_OMg53Z;1o^OLf54Y;0S_OLc54Z;OW_OK]57\\;NX_OJ\\57\\;OQ_OI30_58];Om^OMP64R;7o^OBi58X;Mo^ON00g54Z;Oo^OM01e54\\;Nn^OO00d53_;Mn^O:b5I_;Nn^O24I^57^;0P_O05I\\57_;OQ_O14J[56W;G^_O6O23KY54X;KY_O4513MU52Y;7`_OJ3MS52Z;4c_OM1MP53[;3e_OM1Mn43\\;3e_OM2Lm44[;3g_OM2Lk44[;4h_OL2Lk43\\;4h_OM2Kj44\\;4h_OM3Kh44];4h_OM3Ki43[;6h_OM5Jg42];4j_O02Ke42^;4j_O04Jc42^;5j_O05Jb41^;6j_O07Hb41];6k_O08I_40_;7i_O1:H^4O_;8h_O1<I]4M_;7h_O4>H[4L^;8j_O3>IZ4L];9j_O3`0HX4L_;8i_O3b0IU4L`;8i_O2d0IS4La;9g_O2g0IP4L`;:j_OOi0Jl3Na;8k_O0h0Jl3MVK1R`09U@Nh0Kj3MVK2S`09U@Lh0Mi3LWK2S`08W@Kg0Oo3MS;9[@Ff04l3LR;:hAKk2Kf;;`AIi2Mg;:aAIg2Mg;;cAHe2Ng;9fAHc21d;8jAG`24d;4mAI^2M\\K5W`04QBI[2N_K4U`04SBJX2NaK3T`05TBJU2OdK1S`05UBKT2OeKOR`08VBJQ2NR<8oAJl1MX<:kAIab08`]OHj1MY<<nAGh1MY<=PBFe1NY<<UBEa10X<=XBC^11Y<<[BCZ12Z<;^BCV12\\<<_BAS15]<9cBBn09Z<6jBAi0?Y<NQCBc0:[LLR`07RCC>9bLLn?7SCE;6hLJg?`0XC_O87j<;PC^O48k<9YC_OF8Q=9ZC_OD8R=9ZC@B8S=9\\C_O_O9T=3dCDVO:V=OaCF^L0j2<X=MaCG]L0i2<Z=L`CH]L0i2;\\=K`CJ[O9Y=J\\CNZO7[a0He^O7\\a0Jd^O5]a0Kb^O5_a0Ja^O7^a0J`^O6ba0J^^O5ba0L`[ONh26ia0K\\^O5da0L[^O5ea0K[^O4ea0MZ^O4ea0MZ^O3fa0NY^O2ga0NY^O3ga0MX^O3ha0NW^O2ja0NU^O2ka0OT^O1ma0NS^O2ma0NS^O2na0NR^O1oa0NQ^O2oa0OR^OOoa01Q^ONPb02R^OJoa06n20O0010O010O010O010O001000O010O0100O0100O001O10O1O001000O01000O0100O10O100O10O10O0100O01O10O010O1O0100000O0100000O01000000O010000O1000O10000O010000O0100000O1000O1O100O01O1O011N1Oka`;",
                },
                "bbox": [282, 331, 250, 431],
            },
            {
                "id": 1,
                "image_id": 0,
                "category_id": 0,
                "segmentation": {
                    "size": [768, 1024],
                    "counts": "cVi<5ig08H4L5L5K3M2N2O2M2O1O001O100N101N101O010O002O0O2OAbYO[O]f0U100O1000000kYOaNge0`1XZOaNMNce0a1^ZOlN`e0U1]ZOnNbe0j10O2N1O0O1PNXZO01\\1o0_Ndc0V1\\[OEn0]O`c0m0c[OEm0@dc0f0`[OHk0Dfc0c0`[OG?XOG?Zd0M][O823?]OD=^d0K^[O721>BB>ed0AZ[O?0O?=Yd0ROX[Od0NLa0`0`d05`[OXO@3Pe0c0`[O]O_O0Re0`0_[O5cd0G][O<dd0^O][Oe0dd0ZOZ[Oh0hd0X13L2N3L3N1O1O00O010[OSNU[Oo1gd0WNU[Ok1id0dNW[Oo0hd0QOZ[On0dd0SO^[Ol0ad0TO`[OXOJX1dd0Bc[Oh0]d0YOc[OROI\\1bd0Cg[OPOHd01J_d0b0i[OPOH41f0_d04l[OPOG31f0[d09o[OjNH7Nd0Zd0=[\\OoN[OILe0^d0d0\\\\OnN_O:Ud0k0\\\\OlN^O7Td0P1^\\OlN[O3Pd0h0j[OYOj0M\\O0gc0S1T\\OPOj0M[OFJ3hc0KY\\O`12mNi00[c0X1o[OfNh03Uc0U1W\\OgNGFl0>Sc0T1\\\\OlNc0Oob0T1`\\OnNd0Kib06X\\O:>Eb0Keb06Z\\O;`0Fa0EmNJ_c0h0`\\O5d0Fa0EXb0`1X]OkNb0BWb0b1W]OmNc0@Vb0b1V]OfN]OLX1HWb0f1T]OfN]OLld0[1g[OjN]OKRe0U1a[OoN^OLPe0U1c[OoN\\ONnd0T1f[OoN\\OMcd0^1R\\OeNZONbd0^1U\\OcNYO0bd0Z1X\\OTOgc0k0[\\OUOec0i0^\\OWObc0g0_\\OYOac0f0`\\OZOac0d0a\\O[O^c0e0c\\O[O\\c0e0e\\O[OYc0f0h\\OZOWc0e0k\\O[OUc0b0o\\O\\OSc01b[OG[18Tc0Ld[OLZ17Sc0Kb[O0\\14Pc0Nb[O0_11nb0f0T]OWOmb0Ja[Ob0c1XO^N2dd0N\\[Oh0d1VO^N1bd04[[Oc0o1WOgb0S1S2F:M4L5L6K9F^bW8",
                },
                "bbox": [545, 417, 127, 182],
            },
            {
                "id": 2,
                "image_id": 2,
                "category_id": 1,
                "segmentation": {
                    "size": [768, 1024],
                    "counts": "]]R?4kg02O0O10000O0100O010000O0010O010O00100O1000O10000O010O10O010O1O10000000000000O100O10O1O01000O10000000O100O00010O010O1O01O000010O010O0100O01O1O001O01N110O010ORNMQ\\O2Pd0Oo[O1Qd00m[O1Sd01k[OOUd02i[ONXd02h[ONYd02e[ON]d01c[OO^d01a[ONad01_[OObd01][OOcd02\\[ONed01[[OOed02Z[ONgd01Y[OOhd01V[O0jd00U[O1kd01S[ONod02oZOOQe02nZOMTe02lZOMVe03iZOMYe00iZONYe01gZOO[e0M_f_6",
                },
                "bbox": [643, 78, 104, 100],
            },
        ],
        "info": {},
        "categories": [
            {"id": 0, "name": "weed: broadleaf"},
            {"id": 1, "name": "weed: grass"},
        ],
    }
    assert expected == actual


def test_excess_categories(converter):
    with pytest.raises(ValueError, match="Got 2: #000000, #00ff00"):
        converter.run(
            [
                "--category-map",
                TEST_DATA_DIR / "category_name_cobbity-too_few_mapped.yaml",
            ]
        )


def test_too_many_colors_unmapped(converter):
    with pytest.warns(UserWarning, match="only 2 of these are present"):
        actual = converter.run(
            [
                "--category-map",
                TEST_DATA_DIR / "category_name_cobbity-too_many_mapped.yaml",
            ]
        )
    # TODO: assert re relationship of actual to basic case
