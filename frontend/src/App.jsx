import { useState } from "react";
import axios from "axios";
import {
  LayoutDashboard,
  Building2,
  GitBranch,
  Users,
  UserRound,
  BriefcaseBusiness,
  ClipboardList,
  CalendarCheck,
  CalendarDays,
  FileText,
  Bell,
  ShieldCheck,
  LogOut,
  Menu,
  X,
} from "lucide-react";
import "./App.css";

const API = "http://127.0.0.1:8002";

const menuItems = [
  { id: "dashboard", label: "لوحة التحكم", icon: LayoutDashboard },
  { id: "companies", label: "الشركات", icon: Building2 },
  { id: "branches", label: "الفروع", icon: GitBranch },
  { id: "users", label: "المستخدمون", icon: Users },
  { id: "employees", label: "الموظفون", icon: UserRound },
  { id: "departments", label: "الأقسام", icon: BriefcaseBusiness },
  { id: "tasks", label: "المهام", icon: ClipboardList },
  { id: "attendance", label: "الحضور", icon: CalendarCheck },
  { id: "leaves", label: "الإجازات", icon: CalendarDays },
  { id: "reports", label: "التقارير", icon: FileText },
  { id: "notifications", label: "الإشعارات", icon: Bell },
  { id: "audit", label: "سجل التدقيق", icon: ShieldCheck },
];

function App() {
  const [user, setUser] = useState(null);
  const [dashboard, setDashboard] = useState(null);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [activePage, setActivePage] = useState("dashboard");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [companies, setCompanies] = useState([]);
  const [companyLoading, setCompanyLoading] = useState(false);
  const [companyError, setCompanyError] = useState("");
  const [branches, setBranches] = useState([]);
  const [branchLoading, setBranchLoading] = useState(false);
  const [branchError, setBranchError] = useState("");
  const [users, setUsers] = useState([]);
  const [userLoading, setUserLoading] = useState(false);
  const [userError, setUserError] = useState("");
  const [employees, setEmployees] = useState([]);
  const [employeeLoading, setEmployeeLoading] = useState(false);
  const [employeeError, setEmployeeError] = useState("");

const [tasks, setTasks] = useState([]);
const [taskLoading, setTaskLoading] = useState(false);
const [taskError, setTaskError] = useState("");


const [departments, setDepartments] = useState([]);
const [departmentLoading, setDepartmentLoading] = useState(false);
const [departmentError, setDepartmentError] = useState("");
  const currentPage =
    menuItems.find((item) => item.id === activePage)?.label || "لوحة التحكم";

  const summary = dashboard?.summary || {
    branches: 0,
    employees: 0,
    tasks: 0,
    reports: 0,
    users_active: 0,
  };


  const login = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const loginResponse = await axios.post(
        `${API}/api/v1/auth/login`,
        {
          email: email.trim(),
          password,
        }
      );

      const token = loginResponse.data.access_token;

      if (!token) {
        throw new Error("لم يتم استلام رمز الدخول");
      }

      localStorage.setItem("token", token);

      const dashboardResponse = await axios.get(
        `${API}/api/v1/dashboard/`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setUser(loginResponse.data.user);
      setDashboard(dashboardResponse.data);
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.detail ||
        err.message ||
        "حدث خطأ أثناء تسجيل الدخول"
      );
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
    setDashboard(null);
    setActivePage("dashboard");
  };

  const selectPage = async (page) => {
    setActivePage(page);
    setSidebarOpen(false);

    const token = localStorage.getItem("token");
    if (!token) return;

    const headers = {
      Authorization: `Bearer ${token}`,
    };

    if (page === "companies") {
      setCompanyLoading(true);
      setCompanyError("");

      try {
        const response = await axios.get(
          `${API}/api/v1/companies/`,
          { headers }
        );
        setCompanies(response.data);
      } catch (err) {
        console.error(err);
        setCompanyError(
          err.response?.data?.detail ||
          "تعذر تحميل بيانات الشركة"
        );
      } finally {
        setCompanyLoading(false);
      }
    }

    if (page === "branches") {
      setBranchLoading(true);
      setBranchError("");

      try {
        const response = await axios.get(
          `${API}/api/v1/branches/`,
          { headers }
        );
        setBranches(response.data);
      } catch (err) {
        console.error(err);
        setBranchError(
          err.response?.data?.detail ||
          "تعذر تحميل بيانات الفروع"
        );
      } finally {
        setBranchLoading(false);
      }
    }

    if (page === "users") {
      setUserLoading(true);
      setUserError("");

      try {
        const response = await axios.get(
          `${API}/api/v1/users/`,
          { headers }
        );
        setUsers(response.data);
      } catch (err) {
        console.error(err);
        setUserError(
          err.response?.data?.detail ||
          "تعذر تحميل بيانات المستخدمين"
        );
      } finally {
        setUserLoading(false);
      }
    }

    if (page === "tasks") {
    setTaskLoading(true);
    setTaskError("");

    try {
      const response = await axios.get(
        `${API}/api/v1/tasks/`,
        { headers }
      );
      setTasks(response.data);
    } catch (err) {
      console.error(err);
      setTaskError(
        err.response?.data?.detail ||
        "تعذر تحميل بيانات المهام"
      );
    } finally {
      setTaskLoading(false);
    }
  }

  if (page === "departments") {
    setDepartmentLoading(true);
    setDepartmentError("");

    try {
      const response = await axios.get(
        `${API}/api/v1/departments/`,
        { headers }
      );
      setDepartments(response.data);
    } catch (err) {
      console.error(err);
      setDepartmentError(
        err.response?.data?.detail ||
        "تعذر تحميل بيانات الأقسام"
      );
    } finally {
      setDepartmentLoading(false);
    }
  }

  if (page === "employees") {
      setEmployeeLoading(true);
      setEmployeeError("");

      try {
        const response = await axios.get(
          `${API}/api/v1/employees/`,
          { headers }
        );
        setEmployees(response.data);
      } catch (err) {
        console.error(err);
        setEmployeeError(
          err.response?.data?.detail ||
          "تعذر تحميل بيانات الموظفين"
        );
      } finally {
        setEmployeeLoading(false);
      }
    }
  };

  if (!user) {
    return (
      <main className="login-page" dir="rtl">
        <div className="login-card">
          <div className="brand-icon">
            <Building2 size={30} />
          </div>

          <h1>Central Company</h1>
          <p>نظام الإدارة المركزية للشركات متعددة الفروع</p>

          <form onSubmit={login}>
            <input
              type="email"
              placeholder="البريد الإلكتروني"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />

            <input
              type="password"
              placeholder="كلمة المرور"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />

            {error && <div className="error-box">{error}</div>}

            <button type="submit">
              تسجيل الدخول
            </button>
          </form>
        </div>
      </main>
    );
  }

  return (
    <main className="app-shell" dir="rtl">
      <aside className={`sidebar ${sidebarOpen ? "open" : ""}`}>
        <div className="sidebar-header">
          <div className="brand-icon">
            <Building2 size={25} />
          </div>

          <div>
            <h2>Central Company</h2>
            <span>CCMS</span>
          </div>

          <button
            className="close-sidebar"
            onClick={() => setSidebarOpen(false)}
          >
            <X size={21} />
          </button>
        </div>

        <nav className="sidebar-menu">
          {menuItems.map((item) => {
            const Icon = item.icon;

            return (
              <button
                key={item.id}
                className={`menu-item ${
                  activePage === item.id ? "active" : ""
                }`}
                onClick={() => selectPage(item.id)}
              >
                <Icon size={20} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>

        <div className="sidebar-footer">
          <div className="profile-mini">
            <div className="avatar">
              {user.full_name?.charAt(0) || "U"}
            </div>

            <div>
              <strong>{user.full_name}</strong>
              <span>{user.role}</span>
            </div>
          </div>

          <button className="logout-btn" onClick={logout}>
            <LogOut size={19} />
            تسجيل الخروج
          </button>
        </div>
      </aside>

      {sidebarOpen && (
        <div
          className="sidebar-overlay"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      <section className="main-content">
        <header className="main-header">
          <button
            className="menu-toggle"
            onClick={() => setSidebarOpen(true)}
          >
            <Menu size={23} />
          </button>

          <div>
            <h1>{currentPage}</h1>
            <span>نظام الإدارة المركزية للشركات متعددة الفروع</span>
          </div>

          <div className="header-user">
            <Bell size={21} />
            <div className="header-avatar">
              {user.full_name?.charAt(0) || "U"}
            </div>
          </div>
        </header>

        {activePage === "dashboard" ? (
          <>
            <section className="welcome">
              <div>
                <h2>مرحباً {user.full_name} 👋</h2>
                <p>
                  تابع أداء الشركة وفروعها من لوحة التحكم المركزية.
                </p>
              </div>

              <div className="status-badge">
                <span></span>
                النظام يعمل
              </div>
            </section>

            <section className="cards">
              <div className="card">
                <div className="card-icon">
                  <Building2 />
                </div>
                <span>الفروع</span>
                <strong>{summary.branches}</strong>
              </div>

              <div className="card">
                <div className="card-icon">
                  <UserRound />
                </div>
                <span>الموظفون</span>
                <strong>{summary.employees}</strong>
              </div>

              <div className="card">
                <div className="card-icon">
                  <ClipboardList />
                </div>
                <span>المهام</span>
                <strong>{summary.tasks}</strong>
              </div>

              <div className="card">
                <div className="card-icon">
                  <FileText />
                </div>
                <span>التقارير</span>
                <strong>{summary.reports}</strong>
              </div>

              <div className="card">
                <div className="card-icon">
                  <Users />
                </div>
                <span>المستخدمون النشطون</span>
                <strong>{summary.users_active}</strong>
              </div>

              <div className="card">
                <div className="card-icon">
                  <CalendarCheck />
                </div>
                <span>الحضور اليوم</span>
                <strong>{dashboard.attendance.present}</strong>
              </div>
            </section>

            <section className="info-grid">
              <div className="panel">
                <div className="panel-title">
                  <ClipboardList size={21} />
                  <h3>المهام</h3>
                </div>

                <p>
                  <span>قيد الانتظار</span>
                  <strong>{dashboard.tasks.pending}</strong>
                </p>

                <p>
                  <span>مكتملة</span>
                  <strong>{dashboard.tasks.completed}</strong>
                </p>
              </div>

              <div className="panel">
                <div className="panel-title">
                  <CalendarDays size={21} />
                  <h3>الإجازات</h3>
                </div>

                <p>
                  <span>معلقة</span>
                  <strong>{dashboard.leave_requests.pending}</strong>
                </p>

                <p>
                  <span>موافق عليها</span>
                  <strong>{dashboard.leave_requests.approved}</strong>
                </p>

                <p>
                  <span>مرفوضة</span>
                  <strong>{dashboard.leave_requests.rejected}</strong>
                </p>
              </div>

              <div className="panel">
                <div className="panel-title">
                  <CalendarCheck size={21} />
                  <h3>الحضور</h3>
                </div>

                <p>
                  <span>حاضر</span>
                  <strong>{dashboard.attendance.present}</strong>
                </p>

                <p>
                  <span>متأخر</span>
                  <strong>{dashboard.attendance.late}</strong>
                </p>

                <p>
                  <span>غائب</span>
                  <strong>{dashboard.attendance.absent}</strong>
                </p>
              </div>
            </section>
          </>
        ) : activePage === "tasks" ? (
    <section className="page-section">
      <div className="page-heading">
        <div>
          <h2>المهام</h2>
          <p>إدارة ومتابعة مهام الشركة والموظفين</p>
        </div>
        <span className="page-count">
          {tasks.length} مهمة
        </span>
      </div>

      {taskLoading ? (
        <div className="loading-box">جاري تحميل المهام...</div>
      ) : taskError ? (
        <div className="error-box">{taskError}</div>
      ) : tasks.length === 0 ? (
        <div className="empty-box">لا توجد مهام حالياً</div>
      ) : (
        <div className="company-grid">
          {tasks.map((task, index) => (
            <div
              className="company-card"
              key={task.uuid || index}
            >
              <div className="company-card-header">
                <div className="company-logo">
                  <ClipboardList size={28} />
                </div>

                <span className="company-status active">
                  {task.status || "غير محدد"}
                </span>
              </div>

              <h3>{task.title || "مهمة"}</h3>

              <p className="company-description">
                {task.description || "لا يوجد وصف للمهمة"}
              </p>

              <div className="company-details">
                <div>
                  <span>الأولوية</span>
                  <strong>{task.priority || "—"}</strong>
                </div>

                <div>
                  <span>الحالة</span>
                  <strong>{task.status || "—"}</strong>
                </div>

                <div>
                  <span>UUID</span>
                  <strong className="uuid-text">
                    {task.uuid || "غير متوفر"}
                  </strong>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  ) : activePage === "departments" ? (
    <section className="page-section">
      <div className="page-heading">
        <div>
          <h2>الأقسام</h2>
          <p>إدارة أقسام الشركة والفروع التابعة لها</p>
        </div>
        <span className="page-count">
          {departments.length} قسم
        </span>
      </div>

      {departmentLoading ? (
        <div className="loading-box">جاري تحميل الأقسام...</div>
      ) : departmentError ? (
        <div className="error-box">{departmentError}</div>
      ) : departments.length === 0 ? (
        <div className="empty-box">لا توجد أقسام حالياً</div>
      ) : (
        <div className="company-grid">
          {departments.map((department, index) => (
            <div
              className="company-card"
              key={department.uuid || index}
            >
              <div className="company-card-header">
                <div className="company-logo">
                  <BriefcaseBusiness size={28} />
                </div>

                <span className="company-status active">
                  نشط
                </span>
              </div>

              <h3>{department.name || "قسم"}</h3>

              <p className="company-description">
                {department.description || "لا يوجد وصف للقسم"}
              </p>

              <div className="company-details">
                <div>
                  <span>رقم الفرع</span>
                  <strong>{department.branch_id ?? "—"}</strong>
                </div>

                <div>
                  <span>UUID</span>
                  <strong className="uuid-text">
                    {department.uuid || "غير متوفر"}
                  </strong>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  ) : activePage === "employees" ? (
          <section className="page-section">
            <div style={{padding:"20px",background:"#dbeafe",borderRadius:"12px",marginBottom:"20px"}}>
              صفحة الموظفين تعمل — عدد الموظفين: {employees.length}
            </div>
            <div className="page-heading">
              <div>
                <h2>الموظفون</h2>
                <p>بيانات الموظفين من قاعدة البيانات.</p>
              </div>

              <div className="page-count">
                {employees.length} موظف
              </div>
            </div>

            {employeeLoading && (
              <div className="loading-box">
                جاري تحميل بيانات الموظفين...
              </div>
            )}

            {employeeError && (
              <div className="error-box">
                {employeeError}
              </div>
            )}

            {!employeeLoading && !employeeError && employees.length > 0 && (
              <div className="company-grid">
                {employees.map((employee, index) => (
                  <div className="company-card" key={employee.uuid || index}>
                    <div className="company-card-header">
                      <div className="company-logo">
                        <UserRound size={28} />
                      </div>

                      <span className="company-status active">
                        {employee.status || "نشط"}
                      </span>
                    </div>

                    <h3>
                      {employee.full_name ||
                        employee.name ||
                        employee.employee_code ||
                        "موظف"}
                    </h3>

                    <p className="company-description">
                      {employee.position ||
                        employee.job_title ||
                        employee.department_name ||
                        employee.employee_code ||
                        "بيانات الموظف"}
                    </p>

                    <div className="company-details">
                      <div>
                        <span>الرمز</span>
                        <strong>
                          {employee.employee_code || "—"}
                        </strong>
                      </div>

                      <div>
                        <span>UUID</span>
                        <strong className="uuid-text">
                          {employee.uuid || "غير متوفر"}
                        </strong>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {!employeeLoading && !employeeError && employees.length === 0 && (
              <div className="empty-box">
                لا يوجد موظفون لعرضهم.
              </div>
            )}
          </section>

        ) : activePage === "users" ? (
          <section className="page-section">
            <div className="page-heading">
              <div>
                <h2>المستخدمون</h2>
                <p>بيانات المستخدمين من قاعدة البيانات.</p>
              </div>

              <div className="page-count">
                {users.length} مستخدم
              </div>
            </div>

            {userLoading && (
              <div className="loading-box">
                جاري تحميل بيانات المستخدمين...
              </div>
            )}

            {userError && (
              <div className="error-box">
                {userError}
              </div>
            )}

            {!userLoading && !userError && users.length > 0 && (
              <div className="company-grid">
                {users.map((item) => (
                  <div className="company-card" key={item.uuid}>
                    <div className="company-card-header">
                      <div className="company-logo">
                        <UserRound size={28} />
                      </div>

                      <span className="company-status active">
                        {item.status === "active" ? "نشط" : "غير نشط"}
                      </span>
                    </div>

                    <h3>{item.full_name}</h3>

                    <p className="company-description">
                      {item.email}
                    </p>

                    <div className="company-details">
                      <div>
                        <span>الدور</span>
                        <strong>{item.role}</strong>
                      </div>

                      <div>
                        <span>UUID</span>
                        <strong className="uuid-text">
                          {item.uuid}
                        </strong>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {!userLoading && !userError && users.length === 0 && (
              <div className="empty-box">
                لا يوجد مستخدمون لعرضهم.
              </div>
            )}
          </section>

        ) : activePage === "branches" ? (
          <section className="page-section">
            <div className="page-heading">
              <div>
                <h2>الفروع</h2>
                <p>بيانات الفروع من قاعدة البيانات.</p>
              </div>

              <div className="page-count">
                {branches.length} فرع
              </div>
            </div>

            {branchLoading && (
              <div className="loading-box">
                جاري تحميل بيانات الفروع...
              </div>
            )}

            {branchError && (
              <div className="error-box">
                {branchError}
              </div>
            )}

            {!branchLoading && !branchError && branches.length > 0 && (
              <div className="company-grid">
                {branches.map((branch) => (
                  <div className="company-card" key={branch.uuid}>
                    <div className="company-card-header">
                      <div className="company-logo">
                        <GitBranch size={28} />
                      </div>

                      <span className="company-status active">
                        نشط
                      </span>
                    </div>

                    <h3>{branch.name}</h3>

                    <p className="company-description">
                      {branch.address || "لا يوجد عنوان للفرع."}
                    </p>

                    <div className="company-details">
                      <div>
                        <span>المدينة</span>
                        <strong>{branch.city || "غير محددة"}</strong>
                      </div>

                      <div>
                        <span>UUID</span>
                        <strong className="uuid-text">
                          {branch.uuid}
                        </strong>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {!branchLoading && !branchError && branches.length === 0 && (
              <div className="empty-box">
                لا توجد فروع لعرضها.
              </div>
            )}
          </section>

        ) : activePage === "companies" ? (
          <section className="page-section">
            <div className="page-heading">
              <div>
                <h2>الشركات</h2>
                <p>بيانات الشركة من قاعدة البيانات.</p>
              </div>

              <div className="page-count">
                {companies.length} شركة
              </div>
            </div>

            {companyLoading && (
              <div className="loading-box">
                جاري تحميل بيانات الشركة...
              </div>
            )}

            {companyError && (
              <div className="error-box">
                {companyError}
              </div>
            )}

            {!companyLoading && !companyError && companies.length > 0 && (
              <div className="company-grid">
                {companies.map((company) => (
                  <div className="company-card" key={company.uuid}>
                    <div className="company-card-header">
                      <div className="company-logo">
                        <Building2 size={28} />
                      </div>

                      <span
                        className={
                          company.status === "active"
                            ? "company-status active"
                            : "company-status inactive"
                        }
                      >
                        {company.status === "active"
                          ? "نشطة"
                          : "غير نشطة"}
                      </span>
                    </div>

                    <h3>{company.name}</h3>

                    <p className="company-description">
                      {company.description || "لا يوجد وصف للشركة."}
                    </p>

                    <div className="company-details">
                      <div>
                        <span>الدولة</span>
                        <strong>{company.country}</strong>
                      </div>

                      <div>
                        <span>UUID</span>
                        <strong className="uuid-text">
                          {company.uuid}
                        </strong>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {!companyLoading && !companyError && companies.length === 0 && (
              <div className="empty-box">
                لا توجد شركات لعرضها.
              </div>
            )}
          </section>
        ) : (
          <section className="coming-soon">
            <div className="coming-icon">
              {(() => {
                const item = menuItems.find(
                  (menu) => menu.id === activePage
                );
                const Icon = item?.icon || Building2;
                return <Icon size={42} />;
              })()}
            </div>

            <h2>{currentPage}</h2>
            <p>
              هذه الصفحة ضمن نظام CCMS وسيتم ربطها بالـAPI وقاعدة
              البيانات في المرحلة القادمة.
            </p>

            <span>جاهزة للربط 🚀</span>
          </section>
        )}
      </section>
    </main>
  );
}

export default App;
