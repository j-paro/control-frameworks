from pprint import pprint
import re
import json

import pandas
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.session import Session

from app.models import Framework, Control, FrameworkMappingsPerformed


def get_framework(name, owner, session: Session):
    result = session.execute(
        select(Framework).where(
            and_(Framework.name == name, Framework.owner == owner)
        )
    )
    framework_id = result.scalar_one_or_none()
    return framework_id


def control_mappings_exist(
    mapped_from_framework_id, mapped_to_framework_id, session: Session
):
    result = session.execute(
        select(FrameworkMappingsPerformed).where(
            and_(
                FrameworkMappingsPerformed.mapped_from_framework_id
                == mapped_from_framework_id,
                FrameworkMappingsPerformed.mapped_to_framework_id
                == mapped_to_framework_id,
            )
        )
    )
    framework_mapping: Control = result.scalar_one_or_none()
    if framework_mapping:
        return True
    else:
        return False


def map_cis_to_nist_and_nist_to_cis(session: Session):
    try:
        df = pandas.read_excel(
            "content/control_mappings/CIS_Controls_v8_Mapping_to_NIST_CSF_2_2023.xlsx",
            sheet_name="All CIS Controls & Safeguards",
        )
        pandas.set_option("display.max_rows", None)
        df = df[["CIS Sub-Control", "Subcategory"]]
        df = df.astype({"CIS Sub-Control": "string"})
        df.dropna(inplace=True)
        df.at[34, "CIS Sub-Control"] = "3.10"
        df.at[156, "CIS Sub-Control"] = "13.10"
        df.at[198, "CIS Sub-Control"] = "16.10"

        objs_to_add = []
        cis_to_nist = {}
        nist_to_cis = {}
        mappings = [
            [row[0], row[1]]
            for row in zip(df["CIS Sub-Control"], df["Subcategory"])
        ]
        for mapping in mappings:
            if mapping[0] not in cis_to_nist:
                cis_to_nist[mapping[0]] = []
            cis_to_nist[mapping[0]].append(mapping[1])
            if mapping[1] not in nist_to_cis:
                nist_to_cis[mapping[1]] = []
            nist_to_cis[mapping[1]].append(mapping[0])

        cis_framework = get_framework("CIS CSC", "CIS", session)
        nist_framework = get_framework("NIST CSF", "NIST", session)

        return_due_to_error = False
        if not cis_framework:
            print("Mapping Error: CIS CSC framework not found")
            return_due_to_error = True
        if not nist_framework:
            print("Mapping Error: NIST CSF framework not found")
            return_due_to_error = True
        if control_mappings_exist(cis_framework.id, nist_framework.id, session):
            print(
                "Mapping Error: CIS to NIST CSF control mappings already loaded"
            )
            return_due_to_error = True
        if control_mappings_exist(nist_framework.id, cis_framework.id, session):
            print(
                "Mapping Error: NIST CSF to CIS control mappings already loaded"
            )
            return_due_to_error = True
        if return_due_to_error:
            return

        for key in cis_to_nist:
            result = session.execute(
                select(Control)
                .where(
                    and_(
                        Control.control_string_id == key,
                        Control.framework_id == cis_framework.id,
                    )
                )
                .options(selectinload(Control.control_mappings))
            )
            cis_control: Control = result.scalar_one_or_none()
            if not cis_control:
                raise Exception("CIS control not found: " + key)
            for nist_control_string_id in cis_to_nist[key]:
                result = session.execute(
                    select(Control)
                    .where(Control.control_string_id == nist_control_string_id)
                    .options(selectinload(Control.control_mappings))
                )
                nist_control: Control = result.scalar_one_or_none()
                if not nist_control:
                    raise Exception(
                        "NIST control not found: " + nist_control_string_id
                    )
                cis_control.control_mappings.append(nist_control)

            objs_to_add.append(cis_control)

        for key in nist_to_cis:
            result = session.execute(
                select(Control)
                .where(
                    and_(
                        Control.control_string_id == key,
                        Control.framework_id == nist_framework.id,
                    )
                )
                .options(selectinload(Control.control_mappings))
            )
            nist_control: Control = result.scalar_one_or_none()
            if not nist_control:
                raise Exception("NIST control not found: " + key)
            for cis_control_string_id in nist_to_cis[key]:
                result = session.execute(
                    select(Control)
                    .where(Control.control_string_id == cis_control_string_id)
                    .options(selectinload(Control.control_mappings))
                )
                cis_control: Control = result.scalar_one_or_none()
                if not cis_control:
                    raise Exception(
                        "CIS control not found: " + cis_control_string_id
                    )
                nist_control.control_mappings.append(cis_control)

            objs_to_add.append(nist_control)

        nist_mapping = FrameworkMappingsPerformed(
            mapped_from_framework_id=cis_framework.id,
            mapped_to_framework_id=nist_framework.id,
        )
        cis_mapping = FrameworkMappingsPerformed(
            mapped_from_framework_id=nist_framework.id,
            mapped_to_framework_id=cis_framework.id,
        )
        objs_to_add.append(nist_mapping)
        objs_to_add.append(cis_mapping)

        # pprint(objs_to_add)
        session.add_all(objs_to_add)
        session.commit()
        print("CIS to NIST CSF and NIST CSF to CIS mappings loaded")
    except Exception as e:
        print("Error: ", e)


def map_800_53_to_itself(session: Session):
    try:
        nist_800_53 = get_framework(
            "NIST SP 800-53 Revision 5", "NIST", session
        )

        return_due_to_error = False
        if not nist_800_53:
            print("Mapping Error: NIST SP 800-53 framework not found")
            return_due_to_error = True
        if control_mappings_exist(nist_800_53.id, nist_800_53.id, session):
            print(
                "Mapping Error: NIST 800-53 to itself control mappings already loaded"
            )
            return_due_to_error = True
        if return_due_to_error:
            return

        df = pandas.read_excel(
            "content/SP800_53/sp800-53r5-controls.xlsx",
            sheet_name="SP 800-53 Revision 5",
        )
        df = df[["Control Identifier", "Related Controls"]]
        df.dropna(inplace=True)

        main_list = []
        for _, row in df.iterrows():
            related_controls = row["Related Controls"].split(",")
            related_controls = [control.strip() for control in related_controls]
            main_list.append({row["Control Identifier"]: related_controls})

        # pprint(main_list)

        for mapping in main_list:
            key = next(iter(mapping))
            result = session.execute(
                select(Control)
                .where(Control.control_string_id == key)
                .options(selectinload(Control.control_mappings))
            )
            control: Control = result.scalar_one_or_none()
            if not control:
                print("Mapped from control not found: " + key)
            else:
                for related_control_id in mapping[key]:
                    result = session.execute(
                        select(Control)
                        .where(Control.control_string_id == related_control_id)
                        .options(selectinload(Control.control_mappings))
                    )
                    related_control: Control = result.scalar_one_or_none()
                    if not related_control:
                        print("Mapped to control not found: " + control)
                    else:
                        control.control_mappings.append(related_control)
                        session.add(control)

        session.add(
            FrameworkMappingsPerformed(
                mapped_from_framework_id=nist_800_53.id,
                mapped_to_framework_id=nist_800_53.id,
            )
        )
        session.add(nist_800_53)

        session.commit()
    except Exception as e:
        print("Error: ", e)


def map_800_53_to_nist_csf(session: Session):
    print(
        "*** Mapping NIST SP 800-53 Revision 5 to NIST CSF not implemented yet ***"
    )


def map_nist_csf_to_hipaa(session: Session):
    try:
        return_due_to_error = False
        nist_csf_framework: Framework = get_framework(
            "NIST CSF", "NIST", session
        )
        if not nist_csf_framework:
            print("Mapping Error: NIST CSF framework not found")
            return_due_to_error = True
        hipaa_framework: Framework = get_framework(
            "HIPAA Security Rule Controls", "HHS", session
        )
        if not hipaa_framework:
            print("Mapping Error: HIPAA framework not found")
            return_due_to_error = True
        if control_mappings_exist(
            nist_csf_framework.id, hipaa_framework.id, session
        ):
            print(
                "Mapping Error: NIST CSF to HIPAA control mappings already loaded"
            )
            return_due_to_error = True
        if return_due_to_error:
            return

        csf_to_hipaa_df = pandas.read_excel(
            "content/control_mappings/NIST_CSF_v1.1_core1_HIPAACOW.xlsx",
            sheet_name="NIST CSF HIPAA COW Crosswalk",
        )

        csf_to_hipaa_df = csf_to_hipaa_df[["Subcategory", "HIPAA Reference*"]]
        csf_to_hipaa_df.dropna(inplace=True)

        mappings = []
        for _, row in csf_to_hipaa_df.iterrows():
            key = row["Subcategory"].split(":")[0]
            controls = re.findall(r"164[^\n, ]*", row["HIPAA Reference*"])
            mapping = {key: controls}
            mappings.append(mapping)

        # pprint(mappings)

        nist_controls = set()
        for mapping in mappings:
            key = next(iter(mapping))
            result = session.execute(
                select(Control)
                .where(Control.control_string_id == key)
                .options(selectinload(Control.control_mappings))
            )
            nist_control: Control = result.scalar_one_or_none()
            if not nist_control:
                print("NIST CSF control not found: " + key)
            else:
                for hipaa_control_id in mapping[key]:
                    result = session.execute(
                        select(Control).where(
                            Control.control_string_id == hipaa_control_id
                        )
                    )
                    hipaa_control: Control = result.scalar_one_or_none()
                    if not hipaa_control:
                        print("Control not found: " + hipaa_control_id)
                    else:
                        nist_control.control_mappings.append(hipaa_control)
                        nist_controls.add(nist_control)

        # for nist_control in nist_controls:
        #     pprint("------------------------ Control ------------------------")
        #     pprint(nist_control.control_string_id)
        #     pprint("------------------------ Mappings ------------------------")
        #     pprint(nist_control.control_mappings)

        session.add(
            FrameworkMappingsPerformed(
                mapped_from_framework_id=nist_csf_framework.id,
                mapped_to_framework_id=hipaa_framework.id,
            )
        )
        session.add_all(nist_controls)
        session.commit()
    except Exception as e:
        print("Error: ", e)


def map_csf_to_pci(session: Session):
    try:
        return_due_to_error = False
        nist_framework: Framework = get_framework("NIST CSF", "NIST", session)
        if not nist_framework:
            print("Mapping Error: NIST CSF framework not found")
            return_due_to_error = True
        pci_framework: Framework = get_framework(
            "PCI DSS v3.2.1", "PCI Security Standards Council", session
        )
        if not pci_framework:
            print("Mapping Error: PCI DSS framework not found")
            return_due_to_error = True
        if control_mappings_exist(nist_framework.id, pci_framework.id, session):
            print(
                "Mapping Error: NIST CSF to PCI DSS control mappings already loaded"
            )
            return_due_to_error = True
        if return_due_to_error:
            return

        with open(
            "content/control_mappings/NIST_CSF_to_PCI_DSS.json", "r"
        ) as f:
            csf_to_pci_mappings = json.load(f)

        nist_control_objs = set()
        for csf_control_id, pci_control_ids in csf_to_pci_mappings.items():
            result = session.execute(
                select(Control)
                .where(Control.control_string_id == csf_control_id)
                .options(selectinload(Control.control_mappings))
            )
            csf_control: Control = result.scalar_one_or_none()
            if not csf_control:
                print("NIST CSF control not found: " + csf_control_id)
            else:
                for pci_control_id in pci_control_ids:
                    massaged_id = "PCI DSS " + pci_control_id
                    result = session.execute(
                        select(Control).where(
                            Control.control_string_id == massaged_id
                        )
                    )
                    pci_control: Control = result.scalar_one_or_none()
                    if not pci_control:
                        print("Control not found: " + massaged_id)
                    else:
                        csf_control.control_mappings.append(pci_control)
                        nist_control_objs.add(csf_control)

        # for control_obj in nist_control_objs:
        #     pprint("------------------------ Mappings ------------------------")
        #     pprint(control_obj.control_mappings)

        session.add(
            FrameworkMappingsPerformed(
                mapped_from_framework_id=nist_framework.id,
                mapped_to_framework_id=pci_framework.id,
            )
        )
        session.add_all(nist_control_objs)
        session.commit()
    except Exception as e:
        print("Error: ", e)


def map_nist_to_fcat_controls(session: Session):
    try:
        return_due_to_error = False
        nist_framework: Framework = get_framework("NIST CSF", "NIST", session)
        if not nist_framework:
            print("Mapping Error: NIST CSF framework not found")
            return_due_to_error = True
        fcat_framework: Framework = get_framework(
            "FFIEC Cyber Assessment Tool", "FFIEC", session
        )
        if not fcat_framework:
            print("Mapping Error: FFIEC framework not found")
            return_due_to_error = True
        if control_mappings_exist(
            nist_framework.id, fcat_framework.id, session
        ):
            print(
                "Mapping Error: NIST CSF to FFIEC FCAT control mappings already loaded"
            )
            return_due_to_error = True
        if return_due_to_error:
            return

        with open(
            "content/control_mappings/NIST_CSF_to_FFIEC_FCAT.json", "r"
        ) as f:
            nist_to_fcat_mappings = json.load(f)

        nist_csf_control_objs = set()
        for (
            nist_csf_control_id,
            fcat_control_ids,
        ) in nist_to_fcat_mappings.items():
            result = session.execute(
                select(Control)
                .where(Control.control_string_id == nist_csf_control_id)
                .options(selectinload(Control.control_mappings))
            )
            nist_csf_control: Control = result.scalar_one_or_none()
            if not nist_csf_control:
                pprint("NIST CSF control not found: " + nist_csf_control_id)
            else:
                for fcat_control_id in fcat_control_ids:
                    result = session.execute(
                        select(Control).where(
                            Control.control_string_id == fcat_control_id
                        )
                    )
                    fcat_control: Control = result.scalar_one_or_none()
                    if not fcat_control:
                        pprint("Control not found: " + fcat_control_id)
                    else:
                        nist_csf_control.control_mappings.append(fcat_control)
                        nist_csf_control_objs.add(nist_csf_control)

        # for control_obj in nist_csf_control_objs:
        #     pprint("------------------------ Mappings ------------------------")
        #     pprint(control_obj.control_string_id)

        #     for control_mapping in control_obj.control_mappings:
        #         pprint("   " + control_mapping.control_string_id)

        session.add(
            FrameworkMappingsPerformed(
                mapped_from_framework_id=nist_framework.id,
                mapped_to_framework_id=fcat_framework.id,
            )
        )
        session.add_all(nist_csf_control_objs)
        session.commit()
    except Exception as e:
        print("Error: ", e)


def map_tsc_to_nist_csf(session: Session):
    print("*** Mapping TSC to NIST CSF not implemented yet ***")
