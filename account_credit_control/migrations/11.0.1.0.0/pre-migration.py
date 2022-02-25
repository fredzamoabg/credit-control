# Copyright 2020 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    if openupgrade.table_exists(env.cr, "credit_run_policy_rel"):
        # move data from credit_control_policy_credit_control_run_rel to
        # credit_run_policy_rel
        env.cr.execute(
            """INSERT INTO credit_run_policy_rel
               (run_id, policy_id)
               SELECT credit_control_run_id, credit_control_policy_id
               FROM credit_control_policy_credit_control_run_rel"""
        )
    else:
        openupgrade.rename_tables(
            env.cr,
            [
                (
                    "credit_control_policy_credit_control_run_rel",
                    "credit_run_policy_rel",
                ),
            ],
        )
        openupgrade.rename_columns(
            env.cr,
            {
                "credit_run_policy_rel": [
                    ("credit_control_run_id", "run_id"),
                    ("credit_control_policy_id", "policy_id"),
                ]
            },
        )
