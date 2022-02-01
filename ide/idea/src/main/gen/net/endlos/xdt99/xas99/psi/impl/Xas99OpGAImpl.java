// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xas99.psi.impl;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.lang.ASTNode;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiElementVisitor;
import com.intellij.psi.util.PsiTreeUtil;
import static net.endlos.xdt99.xas99.psi.Xas99Types.*;
import com.intellij.extapi.psi.ASTWrapperPsiElement;
import net.endlos.xdt99.xas99.psi.*;

public class Xas99OpGAImpl extends ASTWrapperPsiElement implements Xas99OpGA {

  public Xas99OpGAImpl(@NotNull ASTNode node) {
    super(node);
  }

  public void accept(@NotNull Xas99Visitor visitor) {
    visitor.visitOpGA(this);
  }

  @Override
  public void accept(@NotNull PsiElementVisitor visitor) {
    if (visitor instanceof Xas99Visitor) accept((Xas99Visitor)visitor);
    else super.accept(visitor);
  }

  @Override
  @Nullable
  public Xas99OpRegister getOpRegister() {
    return findChildByClass(Xas99OpRegister.class);
  }

  @Override
  @Nullable
  public Xas99OpValue getOpValue() {
    return findChildByClass(Xas99OpValue.class);
  }

  @Override
  @Nullable
  public Xas99Sexpr getSexpr() {
    return findChildByClass(Xas99Sexpr.class);
  }

}
