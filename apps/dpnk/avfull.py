# -*- coding: utf-8 -*-
import datetime
from unidecode import unidecode


class Default(dict):
    def __missing__(self, key):
        return ""


def make_address(**fields):
    if not fields.get('tnt_ac_reference'):
        fields['tnt_ac_reference'] = 0
    return u"""\
{m[ac_number]:<15.15}\
{m[name]:<30.30}\
{m[street1]:<30.30}\
{m[street2]:<30.30}\
{m[town]:<30.30}\
{m[county]:<30.30}\
{m[postcode]:<9.9}\
{m[country_code]:<3.3}\
{m[vat_number]:<20.0}\
{m[contact_name]:<22.22}\
{m[phone]:>16.16}\
{m[telex_number]:<7.7}\
{m[fax]:<16.16}\
{m[tnt_ac_reference]:0>9.0f}\
""".format(m=Default(fields))


def make_aline(**fields):
    aline = u"""A\
{m[carrier_code]:<5.5}\
{m[con_reference]:>18.18}\
{m[con_sequence_number]:0>6.0f}\
{m[con_note_number]:0>9.9}\
""".format(m=Default(fields))

    if not fields['delivery_address'] and not fields['pick_up_address'] and not fields['receivers_address'] and not fields['sender_address']:
        return aline
    aline += make_address(**fields['sender_address'])
    if not fields['delivery_address'] and not fields['pick_up_address'] and not fields['receivers_address']:
        return aline
    aline += make_address(**fields['receivers_address'])
    if not fields['delivery_address'] and not fields['pick_up_address']:
        return aline
    aline += make_address(**fields['pick_up_address'])
    if not fields['delivery_address']:
        return aline
    aline += make_address(**fields['delivery_address'])
    return aline


def make_bline(**fields):
    return u"""B\
{m[con_reference]:>18.18}\
{m[con_sequence_number]:0>6.0f}\
{m[con_note_number]:0>9.9}\
{m[con_sending_date]:<8.8}\
{m[special_instructions]:<60.60}\
{m[cost_centre_code]:<20.20}\
{m[service_code]:<5.5}\
{m[payment_indicator]:<1.1}\
{m[sub-service_code1]:<3.3}\
{m[sub-service_code2]:<3.3}\
{m[sub-service_code3]:<3.3}\
{m[sub-service_code4]:<3.3}\
{m[total_no_packages]:0>4}\
{m[weight_in_kg]:0>8.3f}\
{m[currency_code]:<3.3}\
{m[con_total_value]:0>11.3f}\
{m[insurance_value]:<11.11}\
{m[consignment_volume]:<7.7}\
""".format(m=Default(fields))


def make_cline(**fields):
    return u"""C\
{m[con_reference]:>18.18}\
{m[con_sequence_number]:0>6.0f}\
{m[con_note_number]:0>9.9}\
{m[package_type_seq_number]:0>2.0f}\
{m[package_type_desc]:>20.20}\
{m[package_type_count]:<4.0f}\
{m[package_markings]:<10.10}\
{m[package_height]:0>3.0f}\
{m[package_width]:0>3.0f}\
{m[package_depth]:0>3.0f}\
{m[package_type_volume]:<7.7}\
{m[package_total_weight_kgs]:0>8.3f}\
{m[package_reference]:<70.70}\
""".format(m=Default(fields))


def make_dline(**fields):
    return u"""D\
{m[con_reference]:>18.18}\
{m[con_sequence_number]:0>6.0f}\
{m[con_note_number]:0>9.9}\
{m[package_type_seq_number]:0>2.0f}\
{m[article_type_sequence_number]:0>2.0f}\
{m[article_descriptory]:<30.30}\
{m[article_quantity]:<3.3}\
{m[article_weight_kgs]:<8.8}\
{m[article_value]:<11.11}\
{m[article_origin_country]:<3.3}\
{m[export_licence_nr]:<10.10}\
{m[tariff_number]:<15.15}\
{m[hazard_code]:<30.30}\
{m[invoice_desc_line1]:<78.78}\
{m[invoice_desc_line2]:<78.78}\
{m[invoice_desc_line3]:<78.78}\
""".format(m=Default(fields))


def make_avfull(outfile, delivery_batch):
    try:
        today = datetime.datetime.today().strftime("%Y%m%d")
        batch_date = delivery_batch.created.strftime("%y%m%d")
        con_reference = "%s-%s-DPNK" % (str(delivery_batch.pk), batch_date)
        tnt_account_reference = 111057
        for package_transaction in delivery_batch.packagetransaction_set.all():
            user_attendance = package_transaction.user_attendance
            subsidiary = user_attendance.team.subsidiary
            sequence_number = package_transaction.pk

            serviceID = "15N"
            weight = 0.2
            sender_address = {
                "name": "OP Automat",
                "street1": "Korytna 1538/4",
                "town": "PRAHA",
                "postcode": "100 00",
                "country_code": "CZ",
                "tnt_ac_reference": tnt_account_reference,
                }
            receivers_address = {
                "name": u"%s, %s" % (subsidiary.company, subsidiary.address_recipient),
                "contact_name": user_attendance,
                "phone": user_attendance.userprofile.telephone.replace(" ", ""),
                "street1": u"%s %s" % (subsidiary.address_street, subsidiary.address_street_number),
                "town": subsidiary.address_city,
                "postcode": str(subsidiary.address_psc),
                "country_code": "CZ",
                }
            pick_up_address = {}
            delivery_address = {}

            outfile.write(unidecode(make_aline(
                carrier_code="TNT03",
                con_reference=con_reference,
                con_sequence_number=sequence_number,
                con_note_number=package_transaction.tracking_number_cnc(),
                sender_address=sender_address,
                receivers_address=receivers_address,
                pick_up_address=pick_up_address,
                delivery_address=delivery_address,
                )+"\r\n"))

            outfile.write(unidecode(make_bline(
                con_reference=con_reference,
                con_sequence_number=sequence_number,
                con_note_number=package_transaction.tracking_number_cnc(),
                con_sending_date=today,
                service_code=serviceID,
                payment_indicator="S",
                total_no_packages=1,
                currency_code="CZK",
                con_total_value=user_attendance.admission_fee(),
                weight_in_kg=weight,
                )+"\r\n"))

            outfile.write(unidecode(make_cline(
                con_reference=con_reference,
                con_sequence_number=sequence_number,
                con_note_number=package_transaction.tracking_number_cnc(),
                package_type_seq_number=1,
                package_type_desc=user_attendance.campaign.slug,
                package_type_count=1,
                package_height=1,
                package_width=26,
                package_depth=35,
                package_total_weight_kgs=weight,
                )+"\r\n"))

            outfile.write(unidecode(make_dline(
                con_reference=con_reference,
                con_sequence_number=sequence_number,
                con_note_number=package_transaction.tracking_number_cnc(),
                package_type_seq_number=1,
                article_type_sequence_number=1,
                )+"\r\n"))
    finally:
        outfile.close
